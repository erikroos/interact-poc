from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, validators

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")

class NewSeminarForm(FlaskForm):
    name = StringField("Name", validators=[validators.DataRequired()])
    nr_students = IntegerField("Expected number of students")
    submit = SubmitField("Create")