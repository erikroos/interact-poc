from flask import Blueprint, render_template

teachers_blueprint = Blueprint('teachers', __name__, template_folder='templates')

@teachers_blueprint.route("/")
def index():
    return render_template("index_teachers.html")