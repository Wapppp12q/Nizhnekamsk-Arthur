from .registerform import *


class Entrance(FlaskForm):
    email = EmailField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])
    rec = SubmitField('Забыли пароль?')
    submit = SubmitField('Войти')
    reg = SubmitField('Регистрация')
