import os
from pyzbar.pyzbar import decode
from PIL import Image

def detect_barcode_from_image_path(image_path, cropped_image_directory):
    try:

        margin=130
        # Open the image file
        img = Image.open(image_path)
        print(f"Processing image: {image_path}")
        
        # Decode barcodes from the image
        detected_barcodes = decode(img)
        
        barcode_data = []
        # Construct the path for the cropped image directly in the target directory
        base_name = os.path.basename(image_path)
        cropped_image_filename = base_name.replace('barcode','.')
        cropped_image_path = os.path.join(cropped_image_directory, cropped_image_filename)
        
        # Ensure the directory exists
        os.makedirs(cropped_image_directory, exist_ok=True)
        
        # Initialize to track if any barcode was found
        any_barcode_detected = False
        
        for i, barcode in enumerate(detected_barcodes):
            # Get the bounding box coordinates of the barcode
            (x, y, w, h) = barcode.rect
            
            # Expand the bounding box by a small margin
            x = max(0, x - margin)
            y = max(0, y - margin)
            w += 2 * margin
            h += 2 * margin
            
            # Ensure we don't exceed image boundaries
            x_end = min(img.width, x + w)
            y_end = min(img.height, y + h)
            
            barcode_box=[x,y,x_end,y_end]
            # Crop the image to the expanded barcode's bounding box
            
            cropped_img = img.crop((x, y, x_end, y_end))
            
            # Save the cropped image directly in the cropped image directory
            cropped_img.save(cropped_image_path)
            print(f"Cropped barcode image saved at: {cropped_image_path}")

            # Decode barcode data using different encodings
            barcode_text = barcode.data.decode('utf-8', errors='ignore')  # Default utf-8
            try:
                barcode_text = barcode.data.decode('latin-1')  # Latin-1 fallback
            except UnicodeDecodeError:
                pass
            
            barcode_data.append(barcode_text)
            any_barcode_detected = True
        
        if not any_barcode_detected:
            status="NO"
        else:
            status="YES"
        
        return status, barcode_data, cropped_image_path
    
    except Exception as e:
        print(f"Error detecting barcode from image {image_path}: {e}")
