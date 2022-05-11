from .registerform import *
from wtforms import SubmitField


class PageForm(FlaskForm):
    submit = SubmitField('Изменить фотографию')