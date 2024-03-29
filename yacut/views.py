from flask import abort, flash, redirect, render_template

from . import app
from .forms import UrlForm
from .models import URLMap
from .exceptions import DublicateCustomId, NotValidCustomId, MaxIterationDept


@app.route('/<short_id>')
def accept_url_view(short_id):
    url = URLMap.get('short', short_id)
    if url:
        return redirect(url.original)
    abort(404)


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    save_obj = None
    if form.validate_on_submit():
        form_data = {
            'url': form.original_link.data,
            'custom_id': form.custom_id.data,
        }
        obj = URLMap.from_dict(form_data)
        try:
            save_obj = obj.save()
        except (
            DublicateCustomId,
            NotValidCustomId,
            MaxIterationDept,
        ) as error:
            flash(*error.args)
            return render_template('index.html', form=form)

    return render_template('index.html', form=form, data=save_obj)
