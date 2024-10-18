from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm
import random
import string
from .models import URLMap
from . import db

def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choice(characters) for _ in range(length))
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id

@app.route('/')
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data or get_unique_short_id()

        if URLMap.query.filter_by(short=custom_id).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
        else:
            new_url = URLMap(original=original_link, short=custom_id)
            db.session.add(new_url)
            db.session.commit()
            flash(f'Короткая ссылка: {url_for("main.redirect_to_url", short=custom_id, _external=True)}')

    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_url(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)