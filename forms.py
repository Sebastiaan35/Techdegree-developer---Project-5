from flask_wtf import FlaskForm as Form
from wtforms import StringField, DateField, IntegerField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

from models import Journal


class neform(Form):
    Title = StringField("Title", validators=[DataRequired()])
    date  = DateField("Date (yyyy-mm-dd)", validators=[DataRequired()])
    Time_Spent = IntegerField("Time spent (hours as int)", validators=[DataRequired()])
    What_You_Learned = TextAreaField("Learned", validators=[DataRequired()])
    Resources_to_Remember = TextAreaField("To Remember", validators=[DataRequired()])
    tags = StringField("tags (as csv)", validators=[DataRequired()])
