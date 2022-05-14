from wtforms import StringField, SubmitField, PasswordField
from flask_wtf import FlaskForm


class DataForm(FlaskForm):
    name = StringField('Имя:')
    surname = StringField('Фамилия:')
    password = PasswordField('Введите пароль:')
    pass_exam = PasswordField('Подтвердите пароль:')
    submit = SubmitField('Готово')
