import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def insert_data(data, created_at):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("""INSERT INTO public.urls 
        (name, created_at) SELECT %s, %s WHERE NOT EXISTS 
        (SELECT 1 FROM public.urls WHERE name = %s);""", (data, created_at, data,))
        connection.commit()
        connection.close()


def get_data():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.urls ORDER BY id DESC")
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def is_url(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("""SELECT CAST(CASE WHEN EXISTS
         (SELECT 1 FROM public.urls WHERE name = %s)
          THEN 1 ELSE 0 END AS BIT) AS IsUserExist;""", (url,))
        result = curs.fetchone()[0]
        connection.commit()
        connection.close()
        return result


def get_id(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT id FROM public.urls WHERE name = %s;", (url,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def get_id_name_createdat(id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.urls WHERE id = %s;", (id,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def insert_check_id_date(id, created_at):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("INSERT INTO public.url_checks (id, created_at) VALUES (%s, %s);", (id, created_at,))
        connection.commit()
        connection.close()




def insert_check_date_whith_id_site(id, status_code, h1, title, description, created_at):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("INSERT INTO public.url_checks (id, status_code, h1, title, description, created_at) VALUES (%s, %s, %s, %s, %s, %s);",
                     (id, status_code, h1, title, description, created_at,))
        connection.commit()
        connection.close()


def get_check_id():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("""SELECT url_id FROM public.url_checks WHERE id = %s;""")
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def get_data_check(id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.url_checks WHERE id = %s ORDER BY url_id DESC;", (id,))
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def get_data_urls_check():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.url_checks;")
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def get_max_date():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        sql1 = """SELECT id, status_code, MAX(created_at) AS max_created_at FROM public.url_checks GROUP BY id, status_code"""
        curs.execute(sql1)
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result