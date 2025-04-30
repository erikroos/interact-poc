from flask import Blueprint, render_template, request, flash
from interact.students.forms import JoinForm
from interact.teachers.models import Seminar

students_blueprint = Blueprint('students', __name__, template_folder='templates')

@students_blueprint.route("/", methods=["POST", "GET"])
def index():
    form = JoinForm()
    if request.method == "POST":
        if form.validate_on_submit:
            seminar = Seminar.query.filter_by(code=form.code.data, active=True).first()
            if seminar is not None:
                # TODO redirect
                return f"Now joining {seminar.name}"
            else:
                flash("This seminar cannot be joined at the moment")
        else:
            flash("Form not filled in correctly")
    return render_template("index_students.html", form=form)