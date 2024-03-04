from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    save_obj = URLMap.save(data)
    return (
        jsonify(
            {
                'url': save_obj.original,
                'short_link': f'http://localhost/{save_obj.short}',
            }
        ),
        201,
    )


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_original_url(short_id):
    get_obj = URLMap.query.filter_by(short=short_id).first()
    if not get_obj:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': get_obj.original}), 200
