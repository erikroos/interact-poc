from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class JoinForm(FlaskForm):
    code = StringField("Seminar code", validators=[validators.DataRequired()])
    submit = SubmitField("Join")