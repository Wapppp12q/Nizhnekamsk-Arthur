from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField


class Recovery(FlaskForm):
    email = EmailField('Введите почту, на которую зарегистрирован аккаунт:')
    submit = SubmitField('Отправить код')
