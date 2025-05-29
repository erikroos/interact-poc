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