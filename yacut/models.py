from datetime import datetime
import random

from yacut import db

from .error_handlers import InvalidAPIUsage
from .utils import valid_custom_id
from .constants import (
    CHARS_FOR_BULD_URI,
    LENGTH_SHORT_URI,
    SHORT_LENGTH,
    ORIGINAL_LENGTH,
    MAX_ITERATION_DEPT,
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(ORIGINAL_LENGTH), nullable=False)
    short = db.Column(db.String(SHORT_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get_unique_short_id():
        short_url = ''
        data = CHARS_FOR_BULD_URI
        for _ in range(MAX_ITERATION_DEPT):
            short_url = ''.join(random.choices(data, k=LENGTH_SHORT_URI))
            if not URLMap.get('short', short_url):
                return short_url
        raise InvalidAPIUsage(
            'Все возможные вариации коротких ссылок уже существуют'
        )

    @staticmethod
    def get(name, value):
        return URLMap.query.filter_by(**{name: value}).first()

    @staticmethod
    def save(data):
        if 'url' not in data:
            raise InvalidAPIUsage('\"url\" является обязательным полем!')

        if 'custom_id' in data:

            if URLMap.get('short', data['custom_id']):
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )

            if data.get('custom_id') and valid_custom_id(data['custom_id']):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
        if 'custom_id' not in data or not data.get('custom_id'):
            data['custom_id'] = URLMap.get_unique_short_id()

        get_obj = URLMap.get('original', data['url'])
        if get_obj:
            get_obj.short = data['custom_id']
        else:
            get_obj = URLMap()
            get_obj.from_dict(data)
            db.session.add(get_obj)
        db.session.commit()
        return get_obj

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=f'http://localhost/{self.short}',
        )

    def from_dict(self, data):
        attrs_name = {'url': 'original', 'custom_id': 'short'}
        for field in attrs_name:
            if field in data:
                self.__dict__[attrs_name[field]] = data[field]
