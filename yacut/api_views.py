from flask import jsonify, request

from . import app, db
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .utils import shorten_url


@app.route('/api/id/', methods=['POST'])
def add_url():
    data = request.get_json()
    original = data['url']
    custom = data.get('custom_id')

    if original not in data:
        raise InvalidAPIUsage('В запросе отсутствует поле с оригинальной ссылкой')

    if URLMap.query.filter_by(original=original).first() is not None:
        raise InvalidAPIUsage('Эта ссылка уже есть в базе данных')

    if custom is None:
        data['custom_id'] = shorten_url(original)

    url = URLMap()
    url.from_dict(data)
    db.seesion.add(url)
    db.session.commit()
    return jsonify(url.to_dict(), 201)

# @app.route('/api/id>/<int:short_id>/', methods=['POST'])
# def get_url()