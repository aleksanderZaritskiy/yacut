from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import UrlForm
from .models import URLMap


@app.route('/<short_id>')
def accept_url_view(short_id):
    url = URLMap.get('short', short_id)
    if url:
        return redirect(url.original)
    abort(404)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        short_exists = URLMap.get('short', custom_id)
        if not custom_id:
            custom_id = URLMap.get_unique_short_id()
        elif short_exists:
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        get_obj = URLMap.get('original', form.original_link.data)
        if get_obj:
            get_obj.short = custom_id
        else:
            get_obj = URLMap(original=form.original_link.data, short=custom_id)
            db.session.add(get_obj)

        db.session.commit()
        return render_template('index.html', form=form, data=get_obj)
    return render_template('index.html', form=form)
