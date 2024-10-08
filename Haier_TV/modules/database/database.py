import os
import logging
from database.load_database import connect_to_db

def save_data_to_database(record_id, timestamp, barcode_read, barcode_number, 
                          barcode_image, gtv_read, 
                          processed_image, overall_status, database_variables):
    try:
        conn = connect_to_db(database_variables)
        if conn:
            
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO public."GTV" (
                        "RECORD_PRIMARY_ID", 
                        "DATE_TIMESTAMP", 
                        "BARCODE_READ", 
                        "BARCODE_NUMBER", 
                        "BARCODE_IMAGE", 
                        "GTV_READ", 
                        "PROCESSED_IMAGE", 
                        "OVERALL_STATUS"
                    )   
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    [record_id], 
                    [timestamp], 
                    [barcode_read], 
                    barcode_number, 
                    [barcode_image],
                    [gtv_read],
                    # [gtv_image], 
                    # [image_from_camera], 
                    [processed_image], 
                    [overall_status]
                ))
                conn.commit()
                logging.info(f"New Record inserted successfully for barcode: {barcode_number}")
                conn.close()
                return 1
                
        
    except Exception as e:
        logging.error(f"Failed to insert data into database: {e}")
        conn.close()
    
    
      
