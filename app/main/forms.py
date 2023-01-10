from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email

# Forms
class NameForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Start")


class QuestForm(FlaskForm):
    keyword = StringField('Answer', validators=[DataRequired()], render_kw={'autofocus': True})
    submit = SubmitField("Next stage")
