import os
from flask import (Flask, render_template, url_for,
                   request, redirect, flash, get_flashed_messages)
from dotenv import load_dotenv
from datetime import date
from page_analyzer.db_function import (is_url, get_data, insert_data, get_id,
                                       get_id_name_createdat)
import validators
from urllib.parse import urlparse

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls')
def get_sites():
    sites = get_data()
    messages = get_flashed_messages(with_categories=True)
    return render_template('show.html', sites=sites, messages=messages)


@app.route('/urls', methods=['POST'])
def get_site():
    url = request.form.to_dict().get('url')
    if validators.url(url):
        url = urlparse(url).netloc
        if int(is_url(url)):
            flash('Страница уже существует', 'in_base')
        else:
            time = date.today()
            name = url
            insert_data(name, time)
            flash('Страница успешно добавлена', 'added')
        id_name = get_id(url)[0]
        path = f'/urls/{id_name}'
        return redirect(path)
    flash('Некорректный URL', 'nopage')
    return redirect(url_for('index'))


@app.route('/urls/<id>')
def get_site_information(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_id_name_createdat(id)
    if data:
        id, url, time = data[0], data[1], data[2]
        return render_template(
            'new.html',
            id=id, url=url, time=time, messages=messages)
    return render_template('nopage.html')


if __name__ == '__main__':
    app.run()
