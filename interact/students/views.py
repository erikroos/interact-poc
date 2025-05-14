from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from interact import db
from interact.students.forms import JoinForm, JoinWithNameForm, SlideForm
from interact.teachers.models import Seminar, Student, Slide, Answer, Group

students_blueprint = Blueprint('students', __name__, template_folder='templates')

@students_blueprint.route("/", methods=["POST", "GET"])
def index():
    form = JoinForm()
    if request.method == "POST":
        if form.validate_on_submit:
            seminar = Seminar.query.filter_by(code=form.code.data, active=True).first()
            if seminar is not None:
                return redirect(url_for("students.join", id=seminar.id))
            else:
                flash("This seminar cannot be joined at the moment")
        else:
            flash("Form not filled in correctly")
    return render_template("index_students.html", form=form)

@students_blueprint.route("/join/<int:id>", methods=["POST", "GET"])
def join(id:int):
    seminar = Seminar.query.filter_by(id=id).first()
    form = JoinWithNameForm()
    form.name.choices = [(student.id, student.name) for student in seminar.students if student.joined == False]
    if len(form.name.choices) == 0:
        flash("No more spots left in the chosen seminar")
        return redirect(url_for("students.index"))

    if request.method == "POST":
        if form.validate_on_submit:
            student = Student.query.filter_by(id=form.name.data).first()
            if student is not None:
                # Mark student as 'joined' in the DB
                student.joined = True
                student.current_slide = 1
                db.session.commit()
                # Prepare session to track progress
                session["student_id"] = student.id
                session["student_name"] = student.name
                session["seminar_id"] = id
                session["slide"] = 1
                session["score"] = 0

                return redirect(url_for("students.seminar"))
            else:
                flash("Unknown student")
        else:
            flash("Form not filled in correctly")
    return render_template("join.html", form=form, seminar=seminar)

@students_blueprint.route("/seminar", methods=["POST", "GET"])
def seminar():
    current_slide = Slide.query.filter_by(seminar_id=session["seminar_id"], slide_order=session["slide"]).first()
    if current_slide is None:
        # We're out of slides
        flash("Seminar completed!")
        return redirect(url_for("students.index"))
    
    student = Student.query.filter_by(id=session["student_id"]).first()
    seminar = Seminar.query.filter_by(id=session["seminar_id"]).first()
    form = SlideForm()
    
    if current_slide.type == 2:
        # Group forming slide
        if request.method == "GET":
            # Page visit: check if all students have reached this point
            student.reached_gf = True
            db.session.commit()
            nr_students_reached_gf = Student.query.filter_by(seminar_id=seminar.id, reached_gf=True).count()
            if nr_students_reached_gf < seminar.nr_students:
                return render_template("gf_slide_waiting.html", slide=current_slide, nr_slides=len(seminar.slides))
            else:
                from interact.lib.group_forming import GroupForming
                students = Student.query.filter_by(seminar_id=seminar.id).all()
                nr_groups = -(-len(students) // current_slide.gf_nr_per_group) # rounded-up integer division
                groups = [Group(seminar.id, n) for n in range(1, nr_groups+1)]
                db.session.add_all(groups)
                db.session.commit()
                gf = GroupForming(current_slide.gf_nr_per_group, students, groups)
                gf.divide(current_slide.gf_type)
                students = gf.get_students()
                groups = gf.get_groups()
                db.session.commit()
                return render_template("gf_slide_result.html", slide=current_slide, form=form, nr_slides=len(seminar.slides), student=student)
        else:
            # POST, so group forming is complete
            session["slide"] += 1
            student.current_slide += 1
            db.session.commit()
            return redirect(url_for("students.seminar"))

    if request.method == "POST":
        if form.validate_on_submit:
            if current_slide.type == 0:
                # Question slide, check if correct
                answer_id = request.form.get("answer")
                answer = Answer.query.filter_by(id=answer_id).first()
                if answer.correct == True:
                    session["score"] += 1
                    if student.score is None:
                        student.score = 1
                    else:
                        student.score += 1
                    flash(f"Correct answer! Current score: {session["score"]}")
                else:
                    flash(f"Wrong answer... Current score: {session["score"]}")

            session["slide"] += 1
            student.current_slide += 1
            db.session.commit()
            return redirect(url_for("students.seminar"))
        else:
            flash("Form not filled in correctly")
    return render_template("slide.html", slide=current_slide, nr_slides=len(seminar.slides), form=form)