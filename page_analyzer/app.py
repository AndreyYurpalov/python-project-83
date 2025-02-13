import os

import requests
import validators
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
    get_url,
    get_url_check_result,
    get_url_domain,
    get_url_id,
    get_url_inspection_date,
    insert_check_result_with_id_url,
    insert_name_url,
    is_url_in_database,
)
from page_analyzer.functions import (
    get_domain,
    url_parser,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_sites():
    sites = get_url()
    table = get_url_inspection_date()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        sites=sites,
        table=table,
        messages=messages,
    )


@app.route('/urls', methods=['POST'])
def get_site():
    url_for_check = request.form.to_dict().get('url')
    url_length = len(url_for_check)
    url = get_domain(url_for_check)
    if validators.url(url) and url_length <= 255:
        if is_url_in_database(url):
            flash('Страница уже существует', 'info')
            id = get_url_id(url).id
        else:
            insert_name_url(url)
            flash('Страница успешно добавлена', 'success')
            id = get_url_id(url).id
        return redirect(url_for('get_site_information', id=id))
    else:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                           messages=messages, value=url_for_check), 422


@app.route('/urls/<int:id>')
def get_site_information(id):
    messages = get_flashed_messages(with_categories=True)
    data = get_url_domain(id)
    if data:
        id, url, time = data.id, data.name, data.created_at
        table = get_url_check_result(id)
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
    url = get_url_domain(id).name
    try:
        response = requests.get(f'{url}')
        response.raise_for_status()
        status_code, h1, title, description = url_parser(response)
        insert_check_result_with_id_url(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('get_site_information', id=id, ))
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_site_information', id=id, ))
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_site_information', id=id, ))


@app.errorhandler(404)
def no_page(error):
    return render_template('nopage.html'), 404


if __name__ == '__main__':
    app.run()
