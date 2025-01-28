### Hexlet tests and linter status:
[![Actions Status](https://github.com/AndreyYurpalov/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AndreyYurpalov/python-project-83/actions)
[![Test Coverage](https://api.codeclimate.com/v1/badges/715d14638b2ff5ea7c11/test_coverage)](https://codeclimate.com/github/AndreyYurpalov/python-project-83/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/715d14638b2ff5ea7c11/maintainability)](https://codeclimate.com/github/AndreyYurpalov/python-project-83/maintainability)

# Анализатор страниц

Сайт проверки сайтов на SEO-пригодность
Позволяет получить тему, заголовок и описание сайта

Ссылка на web-site: https://python-project-83-3-fzb1.onrender.com

## В проекте использован Python 3.10, Pip 24.3.1, uv 0.5.16

Для разработки использовались следующие инструменты:

Flask — фреймворк для создания веб-приложений на языке программирования Python

Gunicorn — минивеб-сервер, осуществляющий запуск Python-приложения

Requests — библиотека для языка Python, осуществляющая работу с HTTP-запросами

Validators — модуль для проверки данных на соответствие критериям в Pythoт

BeautifulSoup — эбиблиотека Python, используемая для парсинга HTML и XML документов

## Clon project
```python3
git clone https://github.com/AndreyYurpalov/python-project-83.git
cd python-project-83
```
Для хранения конфиденциональной информации создать файл .env в директории 
page-analyzer 

DATABASE_URL = postgresql://{username}{password}@{host}:{port}/{basename}

SECRET_KEY = "{your_secret_key}"

## Instll
```python3
make install
```
## Start localhost
```python3
make dev
```

## Start deploy
```python3
make render-start
```








