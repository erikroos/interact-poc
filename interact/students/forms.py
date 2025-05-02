from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, validators

class JoinForm(FlaskForm):
    code = StringField("Seminar code", validators=[validators.DataRequired()])
    submit = SubmitField("Join")

class JoinWithNameForm(FlaskForm):
    name = SelectField("Choose your name from the list")
    submit = SubmitField("Enter")