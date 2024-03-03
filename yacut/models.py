from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(24), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=f'http://localhost/{self.short}',
        )

    def from_dict(self, data):
        attrs_name = {'url': 'original', 'custom_id': 'short'}
        for field in attrs_name:
            if field in data:
                setattr(self, attrs_name[field], data[field])
