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
    

def get_unique_creation_times(img_dir):
    """Returns a list of unique creation times for images in a directory."""
    try:
        imgs = os.listdir(img_dir)
        creation_time = []
        
        for img in imgs:
            path = os.path.join(img_dir, img)
            cre = os.path.getctime(path)
            cre = time.ctime(cre)
            if cre not in creation_time:
                creation_time.append(cre)
        
        return creation_time

    except Exception as e:
        logging.error(f"Failed to get image time : {e}")

def group_images_by_creation_time(img_dir, img_time):
    try:
    """Groups images based on their creation times."""
        imgs = os.listdir(img_dir)
        curr = []
        for img in imgs:
            path = os.path.join(img_dir, img)
            cre = os.path.getctime(path)
            cre = time.ctime(cre)

            if cre == img_time:
                curr.append(img)
    
        return curr
    except Exception as e:
        logging.error(f"Failed to match the image time - may be pair not found : {e}")
        return None
        

# def process_paths(img_dir):
#     creation_times = get_unique_creation_times(img_dir)
#     creation_times = set(creation_times)  

#     remaining_times = creation_times.copy()

#     for t in list(remaining_times):  
#         imgs = group_images_by_creation_time(img_dir, t)
#         print(f"Processing {imgs}")
#         creation_times.discard(t)  

# process_paths("images")
