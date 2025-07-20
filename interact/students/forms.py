from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, validators

class JoinForm(FlaskForm):
    code = StringField("Seminar code", validators=[validators.DataRequired()])
    submit = SubmitField("Join")

class JoinWithNameForm(FlaskForm):
    name = SelectField("Choose your name from the list")
    motivation = IntegerField("How motivated are you, on a scale from 0-5?", validators=[validators.NumberRange(min=0, max=5)])
    preparation = IntegerField("How well prepared are you, on a scale from 0-5?", validators=[validators.NumberRange(min=0, max=5)])
    submit = SubmitField("Enter")

class SlideForm(FlaskForm):
    submit = SubmitField("Next")