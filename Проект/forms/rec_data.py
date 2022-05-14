from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField


class RDataForm(FlaskForm):
    password = PasswordField('Пароль')
    pass_exam = PasswordField('Поторите пароль')
    submit = SubmitField('Сохранить пароль')