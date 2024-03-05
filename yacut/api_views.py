from flask import jsonify, request

from . import app
from .models import URLMap
from .error_handlers import InvalidAPIUsage
from .exceptions import DublicateCustomId, NotValidCustomId


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    obj = URLMap()
    obj.from_dict(data)
    try:
        save_obj = URLMap.save(obj)
    except (DublicateCustomId, NotValidCustomId) as error:
        raise InvalidAPIUsage(*error.args)
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
    get_obj = URLMap.get('short', short_id)
    if not get_obj:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': get_obj.original}), 200
