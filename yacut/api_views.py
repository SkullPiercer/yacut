from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import shorten_url, is_valid_url
from .constants import MAX_LENGTH

@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or data.get('url') is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    data['original'] = data.get('url')

    if data.get('custom_id') is None or data.get('custom_id') == '':
        data['short'] = shorten_url(data['original'])
    else:
        data['short'] = data.get('custom_id')

    if URLMap.query.filter_by(short=data['short']).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')

    if not is_valid_url(data['short']):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')

    if URLMap.query.filter_by(original=data['original']).first() is not None:
        raise InvalidAPIUsage('Эта ссылка уже есть в базе данных')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201

@app.route('/api/id/<int:short_id>/', methods=['GET'])
def get_original_url(short_id):
    original = URLMap.query.get(short_id)
    if original is None:
        raise InvalidAPIUsage('Ссылки с указанным id не найдено', 404)
    return jsonify(original.to_dict()), 200