from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, ValidationError
from interact.models import User

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