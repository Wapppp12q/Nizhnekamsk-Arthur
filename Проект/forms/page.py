from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class PageForm(FlaskForm):
    status = StringField()
    submit = SubmitField('Изменить фотографию')