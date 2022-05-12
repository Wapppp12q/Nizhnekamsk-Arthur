from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class VerifForm(FlaskForm):
    code_str = StringField('Письмо отправлено')
    submit = SubmitField('Отправить код')