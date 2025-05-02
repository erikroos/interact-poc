from flask import Blueprint, render_template, request, flash, redirect, url_for
from interact import db
from interact.students.forms import JoinForm, JoinWithNameForm
from interact.teachers.models import Seminar, Student

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
    form.name.choices = [(student.id, student.name) for student in seminar.students]
    if request.method == "POST":
        if form.validate_on_submit:
            student = Student.query.filter_by(id=form.name.data).first()
            if student is not None:
                student.joined = True
                db.session.commit()
                return redirect(url_for("students.seminar", seminar_id=seminar.id, student_id=student.id))
            else:
                flash("Unknown student")
        else:
            flash("Form not filled in correctly")
    return render_template("join.html", form=form)

@students_blueprint.route("/seminar/<int:seminar_id>/<int:student_id>")
def seminar(seminar_id:int, student_id:int):
    return f"Welcome {student_id} to {seminar_id}"