import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2
import os
import logging


def preprocess_image(image_path, img_size):
    try:
        img = Image.open(image_path)
        img = img.resize((img_size, img_size))  
        img = np.array(img)
        if img.shape[2] == 4:  
            img = img[:, :, :3]
        img = img.transpose(2, 0, 1)  
        img = img.astype(np.float32) / 255.0
        logging.info(f'Preprocessed image : {image_path}')
        return img
    except Exception as e:
        logging.error(f'Error while preprocessing image : {e}')
        
def load_model(onnx_model_path):
    """ Load ONNX model for inference """
    ort_session = ort.InferenceSession(onnx_model_path)
    # Print the input details to understand what the model expects
    input_name = ort_session.get_inputs()[0].name
    input_shape = ort_session.get_inputs()[0].shape
    print("Model loaded")
    
    return ort_session

def run_inference(ort_session, img):
    """ Run inference on an image """
    input_name = ort_session.get_inputs()[0].name
    
    # Check if the model expects a batch dimension or not
    if len(ort_session.get_inputs()[0].shape) == 4:
        # Add the batch dimension (1, channels, height, width)
        img = np.expand_dims(img, axis=0)
    
    outputs = ort_session.run(None, {input_name: img})
    return outputs[0]  # Assuming outputs[0] contains the detection info

def detect_classes(image_path, onnx_model_path, class_names, img_size=640, confidence_threshold=0.7):
    """ Perform detection on an image and print the results """
    # Load ONNX model
    ort_session = load_model(onnx_model_path)
    
    # Preprocess the image
    img = preprocess_image(image_path, img_size)
    
    # Run inference
    detections = run_inference(ort_session, img)
    # Iterate over detections (for batch size of 1)
    i=0
    confidence=[]
    not_working_conf=[]
    gtv_conf=[]
    haier_conf=[]
    logo_conf=[]
    for detection in detections[0]:
        # print(detection)
        conf = float(detection[4])
        if conf >= confidence_threshold:
            detection_classes_confidence_list=detection[5:]
            #print(f"{detection_classes_confidence_list}")
            not_working_conf.append(float(detection_classes_confidence_list[0]))
            gtv_conf.append(float(detection_classes_confidence_list[1]))
            haier_conf.append(float(detection_classes_confidence_list[2]))
            logo_conf.append(float(detection_classes_confidence_list[3]))
            confidence.append(detection[4])
    if confidence:
        confidence = sum(confidence)/len(confidence)

        not_working_conf = sum(not_working_conf)/len(not_working_conf)
        gtv_conf = sum(gtv_conf)/len(gtv_conf)
        haier_conf = sum(haier_conf)/len(haier_conf)
        logo_conf = sum(logo_conf)/len(logo_conf)
        pred_list = [not_working_conf, gtv_conf, haier_conf, logo_conf]
        #print("Prediction list : ", pred_list)
        idx=pred_list.index(max(pred_list))
        #print("Prediction : ", class_names[idx], f" With confidence : {confidence} for image {image_path}")
    
    # print(pred_list.index(max(pred_list)))
    
        if(idx==0):
            return 'NOT DETECTED'
        else:
            #return class_names[idx].upper()
            return 'DETECTED'

    else:
        return 'NOT DETECTED'

        
def get_prediction(image_path):
    try:
        class_names = ['not_working', 'gtv', 'haier', 'logo']
        onnx_model_path = 'model_2/best.onnx'
        res = detect_classes(image_path, onnx_model_path, class_names)
        logging.info(f"Detection result : {res}")
        return res
        
    except Exception as e:
        logging.error(f'Error while predicting image : {e}')
#get_prediction(image_path, onnx_model_path)
