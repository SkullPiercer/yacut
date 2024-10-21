from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, URL

from .constants import DATA_REQ_MESS, MAX_LENGTH, MIN_LENGTH


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message=DATA_REQ_MESS),
            Length(MIN_LENGTH, 128),
            URL(),
        ]
    )
    custom_id = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(0, MAX_LENGTH),]
    )
    submit = SubmitField('Создать')
