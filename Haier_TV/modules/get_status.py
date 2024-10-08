import logging
import os
from database.load_database import connect_to_db
from dotenv import load_dotenv
def check_database(barcode_number, database_variables):
    try:
        conn = connect_to_db(database_variables)
        if conn:
            try:
                print(f'Barcode Number : {barcode_number}')
                with conn.cursor() as cur:
                    sql = """SELECT "GTV_READ", "BARCODE_NUMBER"
                             FROM public."GTV"
                             WHERE "BARCODE_NUMBER" = %s"""               
                    barcode_number=str(barcode_number[0])
                    array_literal = f'{{{barcode_number}}}'  # Execute the query with a tuple                    
                    print(cur.execute(sql, (array_literal,)))
                    result = cur.fetchone()
                    conn.close()
                    if result:
                        logging.info(f"Barcode {barcode_number} exists in the database.")
                        return 'true'
                    else:
                        logging.info(f"Barcode {barcode_number} does not exist in the database.")
                        return 'false'
            except Exception as e:
                logging.error(f'Failed to fetch data : {e}')
        else:
            return None
    except Exception as e:
        logging.error(f"Database query failed: {e}")
        conn.rollback()
    finally:
        conn.close()  # Ensure the connection is closed



