from flask import jsonify, request

from . import app, db
from .models import URLMap
from .views import get_unique_short_id
from .error_handlers import InvalidAPIUsage
from .utils import valid_custom_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')

    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')

    if 'custom_id' in data:

        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        if data.get('custom_id') and valid_custom_id(data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )

    if 'custom_id' not in data or not data.get('custom_id'):
        data['custom_id'] = get_unique_short_id()

    get_obj = URLMap.query.filter_by(original=data['url']).first()
    if get_obj:
        get_obj.short = data['custom_id']
    else:
        get_obj = URLMap()
        get_obj.from_dict(data)
        db.session.add(get_obj)
    db.session.commit()
    return (
        jsonify(
            {
                'url': get_obj.original,
                'short_link': f'http://localhost/{get_obj.short}',
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
