import os

import psycopg2
import requests
import validators
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

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
connection = psycopg2.connect(DATABASE_URL)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.route('/urls')
def get_sites():
    with connection as con:
        sites = get_url(con)
        table = get_url_inspection_date(con)
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
    print(url)
    if validators.url(url) and url_length <= 255:
        with connection as con:
            if int(is_url_in_database(url, con)):
                flash('Страница уже существует', 'info')
                id = get_url_id(url, con)[0]
            else:
                insert_name_url(url, con)
                flash('Страница успешно добавлена', 'success')
                id = get_url_id(url, con)[0]
            return redirect(url_for('get_site_information', id=id))
    else:
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html',
                           messages=messages, value=url_for_check), 422


@app.route('/urls/<int:id>')
def get_site_information(id):
    messages = get_flashed_messages(with_categories=True)
    with connection as con:
        data = get_url_domain(id, con)
        if data:
            id, url, time = data[0], data[1], data[2]
            table = get_url_check_result(id, con)
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
    with connection as con:
        url = get_url_domain(id, con)[1]
        try:
            response = requests.get(f'{url}')
            response.raise_for_status()
            url_parse = url_parser(response)

            """   url_parse:   status_code, h1, title, description    """

            insert_check_result_with_id_url(id, con, *url_parse)
            flash('Страница успешно проверена', 'success')
            return redirect(url_for('get_site_information', id=id, ))
        except requests.exceptions.RequestException:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('get_site_information', id=id, ))
        except Exception:
            flash('Произошла ошибка при проверке', 'danger')
            return redirect(url_for('get_site_information', id=id, ))


@app.errorhandler(404)
def no_page():
    return render_template('nopage.html'), 404


if __name__ == '__main__':
    app.run()
