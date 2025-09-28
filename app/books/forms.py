from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class BookForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(max=200)])
    authors = StringField('Авторы', validators=[DataRequired(), Length(max=200)])
    publisher = StringField('Издательство', validators=[DataRequired(), Length(max=200)])
    year = IntegerField('Год издания', validators=[DataRequired(), NumberRange(min=1000, max=2100)])
    pages = IntegerField('Страницы', validators=[DataRequired(), NumberRange(min=1)])
    illustrations = IntegerField('Иллюстрации', default=0)
    cost = FloatField('Стоимость', validators=[DataRequired(), NumberRange(min=0)])
    copies_available = IntegerField('Экземпляров', validators=[DataRequired(), NumberRange(min=0)])
    # branch_id = IntegerField('Филиал') # если реализовано полем
    submit = SubmitField('Сохранить')
