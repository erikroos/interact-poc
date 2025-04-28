from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField("Gebruikersnaam", validators=[validators.DataRequired()])
    password = PasswordField("Wachtwoord", validators=[validators.DataRequired()])
    submit = SubmitField("Login")