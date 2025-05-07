from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from interact import db
from interact.students.forms import JoinForm, JoinWithNameForm, SlideForm
from interact.teachers.models import Seminar, Student, Slide

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
                db.session.commit()
                # Prepare session to track progress
                session["student_id"] = student.id
                session["student_name"] = student.name
                session["seminar_id"] = id
                session["slide"] = 1

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
    form = SlideForm()
    if request.method == "POST":
        if form.validate_on_submit:
            session["slide"] += 1
            return redirect(url_for("students.seminar"))
        else:
            flash("Form not filled in correctly")
    return render_template("slide.html", slide=current_slide, form=form)