from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLForm

from .models import URLMap
from . import db
import hashlib

def shorten_url(url):
    short_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"http://127.0.0.1:5000/{short_hash}"

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    print(2)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print(1)
    else:
        print(form.errors)
        print(form.data)
        # original_link = form.original_link.data
        # custom_id = form.custom_id.data or shorten_url(original_link)
        #
        # if URLMap.query.filter_by(short=custom_id).first():
        #     flash('Предложенный вариант короткой ссылки уже существует.')
        # else:
        #     new_url = URLMap(original=original_link, short=custom_id)
        #     db.session.add(new_url)
        #     db.session.commit()
        #     flash(f'Короткая ссылка: {url_for("main.redirect_to_url", short=custom_id, _external=True)}')

    return render_template('index.html', form=form)


@app.route('/<short>')
def redirect_to_url(short):
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)