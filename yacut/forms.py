from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from .constants import DATA_REQ_MESS, MAX_LENGTH, MIN_LENGTH

class URLForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message=DATA_REQ_MESS),
            Length(MIN_LENGTH, MAX_LENGTH),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(MIN_LENGTH, MAX_LENGTH),]
    )
    submit = SubmitField('Добавить')