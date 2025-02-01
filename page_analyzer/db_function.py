import os
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_domain(url: str) -> str:
    domain = '://'.join([urlparse(url).scheme, urlparse(url).netloc])
    return domain


def insert_name_url(name):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_name = """INSERT INTO public.urls 
                                (name) VALUES (%s);"""
        curs.execute(sql_name, (name,))
        connection.commit()
        connection.close()


def get_data():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_select = "SELECT * FROM public.urls ORDER BY id DESC;"
        curs.execute(sql_select)
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def get_id(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_url = "SELECT id FROM public.urls WHERE name = %s;"
        curs.execute(sql_url, (url,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def get_id_name_created_at(_id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_id = "SELECT * FROM public.urls WHERE id = %s;"
        curs.execute(sql_id, (_id,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def get_data_check(_id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_id = """SELECT * FROM public.url_checks 
                      WHERE id = %s ORDER BY url_id DESC;"""
        curs.execute(sql_id, (_id,))
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def get_max_date():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_select = """SELECT id, status_code, MAX(created_at)
                       AS max_created_at FROM public.url_checks 
                       GROUP BY id, status_code"""
        curs.execute(sql_select)
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def is_url(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_url = """SELECT CAST
                     (CASE WHEN EXISTS
                     (SELECT 1 FROM public.urls WHERE name = %s)
                     THEN 1 ELSE 0 END AS BIT);"""
        curs.execute(sql_url, (url,))
        result = curs.fetchone()[0]
        connection.commit()
        connection.close()
        return result


def insert_check_data_with_id_site(_id, status_code, h1, title, description):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql_all_data = """INSERT INTO public.url_checks 
                          (id, url_id, status_code, h1, title, 
                          description)
                          VALUES (%s, default, %s, %s, %s, %s);"""
        curs.execute(sql_all_data,
                     (_id, status_code, h1, title, description,))
        connection.commit()
        connection.close()
