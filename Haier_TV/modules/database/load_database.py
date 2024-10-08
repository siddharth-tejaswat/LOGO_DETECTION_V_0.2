import os
import psycopg2
import time
import logging

def connect_to_db(database_variables):
    dbname=database_variables["dbname"]
    user=database_variables["user"]
    password=database_variables["password"]
    host=database_variables["host"]
    port=database_variables["port"]
    retries = database_variables["retries"]
    delay = database_variables["delay"]
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port)
            logging.info("Database connection established.")
            return conn
        except Exception as e:
            logging.error(f"Attempt {attempt + 1}: Unable to connect to the database: {e}")
            if attempt < retries - 1:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error("Max retries reached. Exiting.")
                return None
