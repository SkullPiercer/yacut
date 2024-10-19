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

    data['original'] = data['url']
    data['short'] = data.get('custom_id') or shorten_url(data['original'])

    if not is_valid_url(data['short']):
        raise InvalidAPIUsage('Неверный формат короткой ссылки!')

    if len(data['short']) > MAX_LENGTH:
        raise InvalidAPIUsage('Ваша ссылка длиннее 16 символов. Не соответствует спецификации')

    if 'url' not in data:
        raise InvalidAPIUsage('В запросе отсутствует поле с оригинальной ссылкой')

    if URLMap.query.filter_by(original=data['original']).first() is not None:
        raise InvalidAPIUsage('Эта ссылка уже есть в базе данных')

    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201

