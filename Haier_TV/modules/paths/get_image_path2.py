import os
import time
import cv2 

# to check if the image exists
def check_image(path):
    if not os.path.exists(path):
        logging.error(f"Image path does not exists : {path}")
        return None
            
    try:
        image = cv2.imread(path)
        if image is None:
            logging.warning(f"Error while loading image")
            return None
        
    except Exception as e:
        logging.error(f"{e}")
        return None
        
    return path
    
            
    
