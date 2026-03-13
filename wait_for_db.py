import time
import psycopg2
import os

DB_NAME = os.getenv("POSTGRES_DB", "retail")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "db")

while True:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=5432
        )
        conn.close()
        print("Database ready!")
        break
    except psycopg2.OperationalError:
        print("Waiting for database...")
        time.sleep(2)