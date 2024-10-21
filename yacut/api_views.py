from flask import jsonify, request

from . import app, db
from .constants import MAX_LENGTH
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import is_valid_url, shorten_url


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json(silent=True)

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data or data.get('url') is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    data['original'] = data.get('url')

    if data.get('custom_id') is None or data.get('custom_id') == '':
        data['short'] = shorten_url(data["original"])

    else:

        if len(data['custom_id']) >= MAX_LENGTH:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        if not is_valid_url(data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

        data['short'] = data.get("custom_id")

    if URLMap.query.filter_by(short=data['short']).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    if URLMap.query.filter_by(original=data['original']).first() is not None:
        raise InvalidAPIUsage('Эта ссылка уже есть в базе данных')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    original = URLMap.query.filter_by(short=short_id).first()
    if original is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original.to_dict()['url']}), 200
