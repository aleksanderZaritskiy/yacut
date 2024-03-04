from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL

from .constants import MIN_LENGHT, SHORT_LENGTH, ORIGINAL_LENGTH


class UrlForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(MIN_LENGHT, ORIGINAL_LENGTH),
            URL(message='Url некорректен'),
        ],
    )
    custom_id = StringField(
        'Ссылка которую хотите получить',
        validators=[Length(MIN_LENGHT, SHORT_LENGTH), Optional()],
    )
    submit = SubmitField('Добавить')
