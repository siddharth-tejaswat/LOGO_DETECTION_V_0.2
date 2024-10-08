import os
import logging
import json 
from database.load_database import connect_to_db
def update_database(barcode_number, 
                    barcode_image, 
                    processed_image,
                    database_variables):
    conn = connect_to_db(database_variables)
    if conn:
        logging.info('Updating Database')
        try:
            barcode_number=str(barcode_number[0])
            array_literal = f'{{{barcode_number}}}'
            #print(f"\n{barcode_image}\n{processed_image}")
            with conn.cursor() as cur:
                sql = """
                    UPDATE public."GTV"
                    SET 
                        "BARCODE_IMAGE" = %s,
                        "PROCESSED_IMAGE" = %s
                    WHERE "BARCODE_NUMBER" = %s
                """
                cur.execute(sql, (   
                    barcode_image, 
                    processed_image, 
                    array_literal
                ))
                conn.commit()
                logging.info(f"Record updated successfully for barcode: {barcode_number}")
                conn.close()
                return 1        
        except Exception as e:            
            logging.error(f"Failed to update data in database: {e}")
            conn.rollback()
            conn.close()
            return 0
