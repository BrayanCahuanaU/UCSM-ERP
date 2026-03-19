import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="dberp",
        user="postgres",
        password="root",
        port="5432"
    )