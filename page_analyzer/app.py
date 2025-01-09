from flask import Flask, request
from dotenv import load_dotenv
import os


load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return 'Hello, World! It is my first progect'