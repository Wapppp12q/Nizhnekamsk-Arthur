from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField
from wtforms import SubmitField, EmailField, IntegerField, StringField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Введите вашу почту', validators=[DataRequired()])
    submit = SubmitField('Отправить код')
    entrance = SubmitField('Уже зарегистрированы?')