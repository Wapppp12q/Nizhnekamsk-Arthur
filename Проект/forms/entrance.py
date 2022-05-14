from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField


class Entrance(FlaskForm):
    email = EmailField('Почта:')
    password = PasswordField('Пароль:')
    rec = SubmitField('Забыли пароль?')
    submit = SubmitField('Войти')
    reg = SubmitField('Регистрация')
