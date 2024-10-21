from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import shorten_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data

        if not original_link.startswith(('http://', 'https://')):
            original_link = 'http://' + original_link

        custom_id = form.custom_id.data or shorten_url(original_link)

        if URLMap.query.filter_by(short=custom_id).first():
            flash(
                'Предложенный вариант короткой ссылки уже существует.', 'error'
            )
        else:
            new_url = URLMap(original=original_link, short=custom_id)
            db.session.add(new_url)
            db.session.commit()
            flash(f'{custom_id}', 'success')

    return render_template('index.html', form=form)


@app.route('/<short>', methods=['GET'])
def redirect_to_url(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)
