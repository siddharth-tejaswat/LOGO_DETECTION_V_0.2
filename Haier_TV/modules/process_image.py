import os
import time
from datetime import datetime 
import shutil
import logging
import PIL
from PIL import Image

from database.database import save_data_to_database
from barcode.detect_barcode_from_image import detect_barcode_from_image_path
from model_2.predict import get_prediction
from database.update_data_to_database import update_database
from database.get_records import get_current_record_details
from get_status import check_database

# to get current time
def get_date_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Function to process a single file and insert into the database
def process_file(barcode_image_path, tv_image_path, processed_image_directory, cropped_images_directory, database_variables):
    try:
        logging.info(f"Processing file: {tv_image_path}")
        # Prepare data
        try:
            record_id = tv_image_path
            timestamp = get_date_timestamp()
            logging.info(f"Detecting barcode from image : {barcode_image_path}")
            #call barcode detection function
            barcode_status, barcode_number, cropped_barcode_image_path = detect_barcode_from_image_path(barcode_image_path, cropped_images_directory)
            logging.info(f"Barcode Detection Status: {barcode_status}, Number: {barcode_number}")
            
            gtv_read = get_prediction(tv_image_path)
            logging.info(f"GTV Read: {gtv_read}, GTV Image Path: {tv_image_path}")
            # Resize the barcode image
            #try:
            #    with Image.open(barcode_image_path) as img:    
            #       resized_image=img.resize((1024,1024), Image.LANCZOS)
            #        resized_image.save(barcode_image_path)
            #    logging.info(f'Resized image {barcode_image_path}')
            #except Exception as e:
            #    logging.error(f'Failed to resize image : {barcode_image_path} \n Error : {e}')  
            try:
                shutil.move(tv_image_path, os.path.join(processed_image_directory, os.path.basename(tv_image_path)))
                logging.info(f"Moved {tv_image_path} to {processed_image_directory}")
                shutil.move(barcode_image_path, os.path.join(cropped_images_directory, os.path.basename(barcode_image_path)))
                logging.info(f"Moved {barcode_image_path} to {cropped_images_directory}")
            except Exception as e:
                logging.error(e)
        
            overall_status = "Processed"
            processed_tv_image_path = os.path.join(processed_image_directory, os.path.basename(tv_image_path))
            processed_barcode_image_path =os.path.join(cropped_images_directory, os.path.basename(barcode_image_path))
            
            barcode_exist = check_database(barcode_number, database_variables)
            print(barcode_exist)
            if barcode_exist=='true':
                # get the existing records in the database
                records=list(get_current_record_details(barcode_number, database_variables))
                barcode_image_lst = records[0].strip('"{}')+ ';' + processed_barcode_image_path
                processed_image_lst = records[1].strip('"{}')+ ';' + processed_tv_image_path
                update_database(
                    barcode_number, 
                    barcode_image_lst, 
                    processed_image_lst,
                    database_variables
                    )
                    #if updated == 1:
                        #logging.info("Record updated successfully")
                    #else:
                    #   logging.info("Failed to update record")
                # Pass all prepared variables to the save_data_to_database function
            else:
                for i in range(0,3):
                    data_saved=save_data_to_database(
                                        record_id, 
                                        timestamp, 
                                        barcode_status,
                                        barcode_number, 
                                        processed_barcode_image_path, 
                                        gtv_read,
                                        processed_tv_image_path, 
                                        overall_status,
                                        database_variables)
                    if data_saved == 1:    
                        logging.info("Data saved to database successfully.")
                        break
                    else:
                        logging.error(f'Database transaction failed')
            logging.info("\n")
        except Exception as e:
            logging.error(f"Error while reading barcode and detecting TV Logo.\n Error : {e}")
            overall_status = "Not Processed"
    except Exception as e:
        logging.error(f"Failed to process file {tv_image_path}: {e}")
        logging.info("\n\n\n")
