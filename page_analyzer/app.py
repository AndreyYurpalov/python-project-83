import os
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
    get_id_name_created_at,
    get_max_date,
    insert_check_data_with_id_site,
    insert_name_url,
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
        id = get_id(url)[0]
        return redirect(url_for('get_site_information', id=id))
    else:
        insert_name_url(url)
        flash('Страница успешно добавлена', 'success')
        id = get_id(url)[0]
        return redirect(url_for('get_site_information', id=id))


@app.route('/urls/<int:id>')
def get_site_information(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_id_name_created_at(id)
    if data:
        id, url, time = data[0], data[1], data[2]
        table = get_data_check(id)
        return render_template(
            'new.html',
            id=id,
            url=url,
            time=time,
            messages=messages,
            table=table,
        )
    return render_template('nopage.html'), 404


@app.route('/urls/<int:id>/checks', methods=['POST'])
def get_check_site(id):
    url = get_id_name_created_at(id)[1]
    try:
        response = requests.get(f'{url}')
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
    else:
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
        insert_check_data_with_id_site(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_site_information', id=id,))


@app.errorhandler(404)
def no_page():
    return render_template('nopage.html'), 404


if __name__ == '__main__':
    app.run()
