import os

from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

from page_analyzer.functions import get_connection

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
connection = get_connection(DATABASE_URL)


def insert_name_url(name):
    with connection as con:
        with con.cursor() as curs:
            sql_name = """INSERT INTO public.urls (name) VALUES (%s);"""
            curs.execute(sql_name, (name,))


def get_url():
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_select = "SELECT * FROM public.urls ORDER BY id DESC;"
            curs.execute(sql_select)
            result = curs.fetchall()
            return result


def get_url_id(url):
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_url = "SELECT id FROM public.urls WHERE name = %s;"
            curs.execute(sql_url, (url,))
            result = curs.fetchone()
            return result


def get_url_domain(_id):
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_id = "SELECT * FROM public.urls WHERE id = %s;"
            curs.execute(sql_id, (_id,))
            result = curs.fetchone()
            return result


def get_url_check_result(_id):
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_id = """SELECT * FROM public.url_checks 
                          WHERE id = %s ORDER BY url_id DESC;"""
            curs.execute(sql_id, (_id,))
            result = curs.fetchall()
            return result


def get_url_inspection_date():
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_select = """SELECT id, status_code, MAX(created_at)
                           AS max_created_at FROM public.url_checks 
                           GROUP BY id, status_code"""
            curs.execute(sql_select)
            result = curs.fetchall()
            return result


def is_url_in_database(url):
    with connection as con:
        with con.cursor(cursor_factory=NamedTupleCursor) as curs:
            sql_url = """SELECT CAST
                         (CASE WHEN EXISTS
                         (SELECT 1 FROM public.urls WHERE name = %s)
                         THEN 1 ELSE 0 END AS BIT);"""
            curs.execute(sql_url, (url,))
            result = int(curs.fetchone().bit)
            return result


def insert_check_result_with_id_url(_id, status_code, h1,
                                   title, description):
    with connection as con:
        with con.cursor() as curs:
            sql_all_data = """INSERT INTO public.url_checks 
                              (id, url_id, status_code, h1, title, 
                              description)
                              VALUES (%s, default, %s, %s, %s, %s);"""
            curs.execute(sql_all_data,
                         (_id, status_code, h1, title, description,))
