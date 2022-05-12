from .registerform import *


class VerifForm(FlaskForm):
    code_str = StringField('Письмо отправлено', validators=[DataRequired()])
    submit = SubmitField('Отправить код')