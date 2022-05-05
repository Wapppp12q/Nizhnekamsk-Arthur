from .registerform import *
from wtforms import FileField


class PageForm(FlaskForm):
    photo = FileField()
    submit = SubmitField('Изменить фотографию')