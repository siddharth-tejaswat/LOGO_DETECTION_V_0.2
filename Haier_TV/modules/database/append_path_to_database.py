import logging

from database.update_data_to_database import update_database
from database.get_records import get_current_record_details

# append paths to the existing paths in the database

def create_new_path(path, next_path):
    path=path.strip('"{}')
    path = path + ';' + next_path
    return str(path)

def append_paths(
        barcode_number,
        barcode_image,
        processed_image):
    try:
        # get the existing records in the database
        records=list(get_current_record_details(barcode_number))
        # append new paths 
        # gtv_image = records[0] 
        # gtv_image=create_new_path(records[0], gtv_image)

        logging.info("Successfully fetched existing records")
    
    except Exception as e:
        logging.error("Failed to fetch existing records")

    try:
        barcode_image = create_new_path(records[0], barcode_image)
        # camera_image = create_new_path(records[2], camera_image)
        processed_image= create_new_path(records[1], processed_image)

        logging.info("Successfully created new records")
        return barcode_image, processed_image
    
    except Exception as e:
        logging.error('Failed to append paths : {e}')
        return None

# update existing paths in the database
def update_paths(barcode_number, 
                cropped_barcode_image_path, 
                processed_image):

    try:
        # append the new paths to the existing paths 
        cropped_barcode_image_path, processed_image=append_paths(
                                                                barcode_number,
                                                                cropped_barcode_image_path,
                                                                processed_image)
        
    except Exception as e:
        logging.error(f'{e}')
        return
    
    # if records fetched update the current record in the database
    try:
        updated=update_database(
                barcode_number, 
                cropped_barcode_image_path, 
                processed_image
                )
        if updated == 1:
            logging.info("Record updated successfully")
        
        else:
            logging.info("Failed to update record")
    
    # if updating records has failed
    except Exception as e:
        logging.error("Failed to update database")


# barcode_number = ['1001963424']
# records=append_paths(barcode_number,'IMAGE','IMAGE', 'IMAGE', 'IMAGE')
# for i in records:
#     print(i)