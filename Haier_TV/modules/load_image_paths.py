import os 
import time 
import logging
import cv2  
from process_image import process_file
def process_paths(img_dir, database_variables):
    base_dir = os.getenv('BASE_PUBLIC_FOLDER')
    barcode_image_directory = os.getenv('APP_PUBLIC_FOLDER_BARCODE')
    tv_image_directory = os.getenv('APP_PUBLIC_FOLDER_TV')
    pictures_dir=os.getenv('RECIEVING_PATH')
    try:
        ac64_image_files = os.listdir(pictures_dir)
        ac64_image_files.sort(key=lambda x:os.path.getctime(os.path.join(pictures_dir,x)), reverse=True)
        ac64_image_files = [f for f in ac64_image_files if "ac64" in f]
        for current_image in list(ac64_image_files):
            image = cv2.imread(os.path.join(pictures_dir,current_image))
            current_barcode_image_path=os.path.join(pictures_dir,current_image)
            current_tv_image_path = os.path.join(pictures_dir, current_image.replace('ac64_cambar', 'ac16_camtv'))
            #print(f"Barcode Image Path : {current_barcode_image_path}")
            #print(f"Camera Image Path : {current_tv_image_path}")
            if image is not None:
                if cv2.imread(current_tv_image_path) is not None:
                    process_file(current_barcode_image_path, current_tv_image_path, tv_image_directory, barcode_image_directory, database_variables)
                else:
                    logging.error(f"Unable to find ac16 image using CV2.")
            else:
                logging.error(f"Unable to find ac64 image using CV2.")
    except Exception as e:
        logging.error(f"Error while processing current image {current_barcode_image_path}. \n Error Message : {e}")
