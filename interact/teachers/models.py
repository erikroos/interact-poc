from interact import db
from flask_login import UserMixin
from interact.teachers.helpers import generate_code

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    seminars = db.relationship("Seminar", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Seminar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user = db.relationship("User", back_populates="seminars")
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=False)
    nr_students = db.Column(db.Integer)
    students = db.relationship("Student", back_populates="seminar", cascade="all, delete-orphan", passive_deletes=True)
    slides = db.relationship("Slide", back_populates="seminar", order_by="Slide.slide_order", cascade="all, delete-orphan", passive_deletes=True)
    groups = db.relationship("Group", back_populates="seminar", cascade="all, delete-orphan", passive_deletes=True)

    def __init__(self, name, nr_students, user_id):
        self.code = generate_code()
        self.name = name
        self.nr_students = nr_students
        self.user_id = user_id
        self.active = False

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_id'], ['user.id'],
            ondelete='CASCADE',
            name='fk_seminar_user'
        ),
    )

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    joined = db.Column(db.Boolean, default=False)
    seminar_id = db.Column(db.Integer)
    seminar = db.relationship("Seminar", back_populates="students")
    score = db.Column(db.Integer, default=0)
    current_slide = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer)
    group = db.relationship("Group", back_populates="students")
    reached_gf = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['seminar_id'], ['seminar.id'],
            ondelete='CASCADE',
            name='fk_student_seminar'
        ),
        db.ForeignKeyConstraint(
            ['group_id'], ['group.id'],
            ondelete='CASCADE',
            name='fk_student_group'
        ),
    )

    def __init__(self, name, seminar_id):
        self.name = name
        self.joined = False
        self.seminar_id = seminar_id

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    students = db.relationship("Student", back_populates="group", cascade="all, delete-orphan", passive_deletes=True)
    seminar_id = db.Column(db.Integer)
    seminar = db.relationship("Seminar", back_populates="groups")

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['seminar_id'], ['seminar.id'],
            ondelete='CASCADE',
            name='fk_group_seminar'
        ),
    )

    def __init__(self, seminar_id, number):
        self.seminar_id = seminar_id
        self.number = number

class Slide(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False, default=0) # 0 = question slide, 1 = text slide, 2 = group forming slide (more types may follow)
    title = db.Column(db.String(100)) # for question OR text heading
    text = db.Column(db.String(500), nullable=True)
    slide_order = db.Column(db.Integer)
    seminar_id = db.Column(db.Integer)
    seminar = db.relationship("Seminar", back_populates="slides")
    answers = db.relationship("Answer", back_populates="slide", cascade="all, delete-orphan", passive_deletes=True)
    gf_type = db.Column(db.Integer, nullable=True) # 0 = random, 1 = mix-level, 2 = same-level
    gf_nr_per_group = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['seminar_id'], ['seminar.id'],
            ondelete='CASCADE',
            name='fk_slide_seminar'
        ),
    )

    def __init__(self, type, title, slide_order, seminar_id, text=None):
        self.type = type
        self.title = title
        self.slide_order = slide_order
        self.text = text
        self.seminar_id = seminar_id

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    correct = db.Column(db.Boolean)
    slide_id = db.Column(db.Integer)
    slide = db.relationship("Slide", back_populates="answers")

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['slide_id'], ['slide.id'],
            ondelete='CASCADE',
            name='fk_answer_slide'
        ),
    )

    def __init__(self, text, correct, slide_id):
        self.text = text
        self.correct = correct
        self.slide_id = slide_id