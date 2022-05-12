from .registerform import *
from wtforms import SubmitField


class PageForm(FlaskForm):
    status = StringField()
    submit = SubmitField('Изменить фотографию')