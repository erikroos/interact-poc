from flask import Flask

app = Flask(__name__)

from interact.students.views import students_blueprint
app.register_blueprint(students_blueprint, url_prefix="/students")

from interact.teachers.views import teachers_blueprint
app.register_blueprint(teachers_blueprint, url_prefix="/teachers")