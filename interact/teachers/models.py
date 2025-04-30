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

    def __init__(self, name):
        self.code = generate_code()
        self.name = name
        self.active = False