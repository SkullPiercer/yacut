from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm

from .models import URLMap
from . import db
from .utils import shorten_url


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data or shorten_url(original_link)

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            new_url = URLMap(original=original_link, short=custom_id)
            db.session.add(new_url)
            db.session.commit()
            flash(f'Короткая ссылка: {custom_id}')

    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_url(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.url)