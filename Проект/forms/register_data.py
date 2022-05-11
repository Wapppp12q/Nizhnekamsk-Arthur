from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class DataForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    password = PasswordField('Введите пароль:')
    pass_exam = PasswordField('Подтвердите пароль:')
    submit = SubmitField('Готово')
