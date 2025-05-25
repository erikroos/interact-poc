from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, validators, ValidationError
from interact.teachers.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.EqualTo('pass_confirm', message='Passwords must match')])
    pass_confirm = PasswordField('Confirm password', validators=[validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username not available')

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