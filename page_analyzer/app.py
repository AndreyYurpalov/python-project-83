import os
from datetime import date
from urllib.parse import urlparse

import requests
import validators
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)

from page_analyzer.db_function import (
    get_data,
    get_data_check,
    get_id,
    get_id_name_createdat,
    get_max_date,
    insert_check_date_whith_id_site,
    insert_data,
    is_url,
)

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
    table = get_max_date()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        sites=sites,
        table=table,
        messages=messages,
    )


@app.route('/urls', methods=['POST'])
def get_site():

    url = request.form.to_dict().get('url')
    if not validators.url(url):
        flash('Некорректный URL', 'no_page')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                               messages=messages, value=url), 422
    url = f'{urlparse(url).scheme}://{urlparse(url).netloc}'
    if int(is_url(url)):
        flash('Страница уже существует', 'info')
    else:
        name = url
        created_at = date.today()
        insert_data(name, created_at)
        flash('Страница успешно добавлена', 'success')
    id = get_id(url)[0]
    return redirect(url_for('get_site_information', id=id))


@app.route('/urls/<id>', methods=['GET'])
def get_site_information(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_id_name_createdat(id)
    if data:
        data = get_id_name_createdat(id)
        check_time = data[2]
        name = data[1]
        insert_data(name, check_time)
        id, url, time = data[0], data[1], data[2]
        table = get_data_check(id)
        check = f'/urls/{id}/checks'
        return render_template(
            'new.html',
            id=id,
            url=url,
            time=time,
            messages=messages,
            table=table,
            check=check,)
    return render_template('nopage.html')


@app.route('/urls/<id>/checks', methods=['POST'])
def get_check_site(id):
    id = int(id)
    url = get_id_name_createdat(id)[1]
    try:
        response = requests.get(f'{url}')
        soup = BeautifulSoup(response.text, 'html.parser')
        h1 = ''
        if soup.find('h1'):
            h1 = soup.find('h1').text
        title = ''
        if soup.find('title'):
            title = soup.find('title').text
        meta_tags = soup.find_all('meta')
        description = ''
        for tag in meta_tags:
            if tag.get('name') == 'description':
                description = tag.get('content')
        status_code = response.status_code
        time_check = date.today()
        insert_check_date_whith_id_site(id, status_code, h1, title,
                                        description, time_check)
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_site_information', id=id,))


if __name__ == '__main__':
    app.run()
