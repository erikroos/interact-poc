from flask import Blueprint, render_template

students_blueprint = Blueprint('students', __name__, template_folder='templates')

@students_blueprint.route("/")
def index():
    return render_template("index_students.html")