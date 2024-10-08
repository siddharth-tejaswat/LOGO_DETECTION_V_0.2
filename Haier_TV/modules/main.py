import os
import sys
import time
import logging

from database.load_database import connect_to_db
from load_image_paths import process_paths
from dotenv import load_dotenv

# Reading environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # You can change to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/logs.log"),  # Log to a file
        logging.StreamHandler(sys.stdout)  # Log to the console
    ]
)

# Main function
if __name__=="__main__":
    logging.info("Initiating barcode and TV logo detection application.")
    img_dir=os.getenv('RECIEVING_PATH')  
    base_dir = os.getenv('APP_PUBLIC_FOLDER')
    # Initialize database variables
    database_variables={"dbname":"postgres", "user":"postgres", "password":"systemzero", "host":"127.0.0.1", "port":"5432", "retries": 5, "delay": 2}
    #barcode_image_directory = os.getenv('APP_PUBLIC_FOLDER_BARCODE')
    #tv_image_directory = os.getenv('APP_PUBLIC_FOLDER_TV')
    # Check database connectivity
    conn = connect_to_db(database_variables)
    if conn:
        conn.close()
        # Start monitoring the directory with stop condition
        while True:  
            try:
                files = os.listdir(img_dir)
                if files is not None:
                    time.sleep(3)
                    process_paths(img_dir, database_variables)
                if not files:
                    logging.warning(f"No files found in the directory: {img_dir}\n Retrying after 5 seconds")
                time.sleep(5)
            except FileNotFoundError:
                logging.error(f"The directory {img_dir} does not exist.")
                break
            except Exception as e:
                logging.exception(f"An error occurred while monitoring the directory: {e}")
                break
    else:
        logging.error("Unable to establish a database connection after multiple attempts.")

    logging.info("Shutting down barcode detection.")  # Log when the function exits
