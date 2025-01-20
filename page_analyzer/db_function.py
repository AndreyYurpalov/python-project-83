import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def insert_data(data, today):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("""INSERT INTO public.new_urls 
        (name, created_at) SELECT %s, %s WHERE NOT EXISTS 
        (SELECT 1 FROM public.new_urls WHERE name = %s);""", (data, today, data))
        connection.commit()
        connection.close()


def get_data():
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.new_urls ORDER BY id DESC")
        result = curs.fetchall()
        connection.commit()
        connection.close()
        return result


def is_url(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("""SELECT CAST(CASE WHEN EXISTS
         (SELECT 1 FROM public.new_urls WHERE name = %s)
          THEN 1 ELSE 0 END AS BIT) AS IsUserExist;""", (url,))
        result = curs.fetchone()[0]
        connection.commit()
        connection.close()
        return result


def get_id(url):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT id FROM public.new_urls WHERE name = %s;", (url,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result


def get_id_name_createdat(id):
    connection = psycopg2.connect(DATABASE_URL)
    with connection.cursor() as curs:
        curs.execute("SELECT * FROM public.new_urls WHERE id = %s;", (id,))
        result = curs.fetchone()
        connection.commit()
        connection.close()
        return result
