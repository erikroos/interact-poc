from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, validators

class NewSeminarForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired()])
    nr_students = IntegerField("Expected number of students")
    submit = SubmitField("Create")

class EnrollForm(FlaskForm):
    submit = SubmitField("Enroll")

class NewSlideForm(FlaskForm):
    title = StringField("Title", validators=[validators.DataRequired(), validators.Length(max=100)])
    text = TextAreaField("Text", validators=[validators.Length(max=500)])
    submit = SubmitField("Add")

class DemoSeminarForm(FlaskForm):
    nr_students_at_gf = IntegerField("Number of students who have reached the Group Forming slide", validators=[validators.NumberRange(min=0, max=5)])
    submit = SubmitField("Create")