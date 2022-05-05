from .registerform import *


class DataForm(FlaskForm):
    name = StringField('Имя:', validators=[DataRequired()])
    surname = StringField('Фамилия:', validators=[DataRequired()])
    password = PasswordField('Введите пароль:', validators=[DataRequired()])
    pass_exam = PasswordField('Подтвердите пароль:', validators=[DataRequired()])
    submit = SubmitField('Готово')
