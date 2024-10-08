import os
import sys

def create_directories(base_dir):
    # Predefined directory names
    dir1 = "cropped_barcode_images"
    # dir2 = "image_from_camera"
    dir3 = "processed_images"
    # dir4 = "tv_image"
    
    # Full paths for the directories
    path1 = os.path.join(base_dir, dir1)
    path3 = os.path.join(base_dir, dir3)
    
    try:
        # Create the directories
        os.makedirs(path1, exist_ok=True)
        os.makedirs(path3, exist_ok=True)
        print("Created dirs:", path1, path3)
    
    except OSError as e:
        # Print the error and terminate the process if directory creation fails
        print(f"Error: {e}")
        sys.exit(1)  # Exit the program with a non-zero status

    return path1, path3