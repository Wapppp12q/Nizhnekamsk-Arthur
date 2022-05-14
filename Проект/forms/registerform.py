from flask_wtf import FlaskForm
from wtforms import SubmitField, EmailField


class RegisterForm(FlaskForm):
    email = EmailField('Введите вашу почту')
    submit = SubmitField('Отправить код')
    entrance = SubmitField('Уже зарегистрированы?')