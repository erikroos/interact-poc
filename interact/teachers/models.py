from interact import db
from flask_login import UserMixin
from interact.teachers.helpers import generate_code

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=False)
    nr_students = db.Column(db.Integer)
    students = db.relationship("Student", back_populates="seminar")

    def __init__(self, name, nr_students):
        self.code = generate_code()
        self.name = name
        self.nr_students = nr_students
        self.active = False

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    seminar_id = db.Column(db.Integer, db.ForeignKey("seminar.id"))
    seminar = db.relationship("Seminar", back_populates="students")

    def __init__(self, name, seminar_id):
        self.name = name
        self.seminar_id = seminar_id