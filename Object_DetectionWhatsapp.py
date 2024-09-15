import cv2
import numpy as np
import urllib.request
import pywhatkit as kit
import time
import os

url = 'http://192.168.98.8/cam-hi.jpg'
whatsapp_number = '+917007864516'  # Replace with your WhatsApp number in international format

# Load YOLO model
modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # Use CPU backend

# Read class names
classesfile = 'coco.names'
classNames = []
with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

def detect_motion(current_frame, prev_frame):
    if prev_frame is None:
        return current_frame, False
    
    frame_diff = cv2.absdiff(current_frame, prev_frame)
    gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        if cv2.contourArea(contour) > 5000:
            return current_frame, True
    return current_frame, False

def find_objects(outputs, img, motion_detected):
    hT, wT, _ = img.shape
    bbox = []
    classIds = []
    confs = []
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > 0.5:
                w, h = int(det[2] * wT), int(det[3] * hT)
                x, y = int((det[0] * wT) - w / 2), int((det[1] * hT) - h / 2)
                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))
    
    indices = cv2.dnn.NMSBoxes(bbox, confs, 0.5, 0.3)
    
    person_detected = False
    if len(indices) > 0:
        indices = indices.flatten()
        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            label = classNames[classIds[i]]
            confidence = int(confs[i] * 100)
            color = (0, 255, 0) if confidence > 80 else (0, 255, 255) if confidence > 60 else (0, 0, 255)
            text = f'{label.upper()} {confidence}%'
            if motion_detected:
                text += ' - Motion Detected'
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            if label == 'person':
                person_detected = True
    
    return img, person_detected

whT = 320
prev_frame = None

while True:
    img_resp = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    
    # Get output layer names
    layernames = net.getLayerNames()
    outputLayers = net.getUnconnectedOutLayers()
    
    if isinstance(outputLayers, list):
        outputNames = [layernames[i - 1] for i in outputLayers]
    else:
        outputNames = [layernames[i - 1] for i in outputLayers.flatten()]
    
    outputs = net.forward(outputNames)
    
    img, motion_detected = detect_motion(img, prev_frame)
    img, person_detected = find_objects(outputs, img, motion_detected)
    
    if motion_detected:
        cv2.putText(img, 'Motion Detected!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    if person_detected:
        # Save the image
        img_name = 'detected_person.jpg'
        cv2.imwrite(img_name, img)
        
        # Send the image via WhatsApp
        kit.sendwhats_image(whatsapp_number, img_name, "Person detected", 10)
        
        # Optional: delete the image after sending
        os.remove(img_name)
    
    cv2.imshow('Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
