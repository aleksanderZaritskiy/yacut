import string
import random

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URLMap


def get_unique_short_id():
    short_url = ''
    data = string.ascii_letters + string.digits
    for _ in range(6):
        short_url += random.choice(data)
    if URLMap.query.filter_by(short=short_url).first():
        return get_unique_short_id()
    return short_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        short_exists = URLMap.query.filter_by(short=custom_id).first()
        if not custom_id:
            custom_id = get_unique_short_id()
        elif short_exists:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        get_obj = URLMap.query.filter_by(
            original=form.original_link.data
        ).first()
        if get_obj:
            get_obj.short = custom_id
        else:
            get_obj = URLMap(original=form.original_link.data, short=custom_id)
            db.session.add(get_obj)

        db.session.commit()
        return render_template('index.html', form=form, data=get_obj)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def accept_url_view(short_id):
    url = URLMap.query.filter_by(short=short_id).first()
    if url:
        return redirect(url.original)
    abort(404)
