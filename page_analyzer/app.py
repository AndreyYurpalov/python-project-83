from flask import Flask, render_template
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

DATABASE_URL = os.getenv('DATABASE_URL')


connection = psycopg2.connect(DATABASE_URL)

if connection:
    print('Connection OK')
connection.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_sites():
    return render_template('show.html')


@app.route('/urls/1')
def get_sites_new():
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debag=True)
