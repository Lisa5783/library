from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class BranchForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired(), Length(max=200)])
    location = StringField('Адрес', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Сохранить')
