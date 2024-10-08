import os   
import logging
from database.load_database import connect_to_db
def get_current_record_details(barcode_number, database_variables):
    conn = connect_to_db(database_variables)
    if conn:
        try:
            with conn.cursor() as cur:
                sql = """SELECT "BARCODE_IMAGE", "PROCESSED_IMAGE"
                         FROM public."GTV"
                         WHERE "BARCODE_NUMBER" = %s"""
                barcode_number=str(barcode_number[0])
                array_literal = f'{{{barcode_number}}}'
                # Execute the query with a tuple
                cur.execute(sql, (array_literal,))
                result = cur.fetchone()
                conn.close()
                if result:
                    logging.info(f"Barcode {barcode_number} exists in the database.")
                    return result  # Return the record details
                else:
                    logging.info(f"Barcode {barcode_number} does not exist in the database.")
                    return None
        except Exception as e:
            logging.error(f"Database query failed: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()  # Ensure the connection is closed

