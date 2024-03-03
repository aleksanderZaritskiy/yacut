from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, URL


class UrlForm(FlaskForm):
    original_link = URLField(
        'Добавьте ссылку',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Url некорректен'),
        ],
    )
    custom_id = StringField(
        'Ссылка которую хотите получить',
        validators=[Length(1, 16), Optional()],
    )
    submit = SubmitField('Добавить')
