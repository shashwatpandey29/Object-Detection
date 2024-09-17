import cv2
import numpy as np
import urllib.request
import winsound

# URL for the ESP32-CAM feed
url = 'http://192.168.244.8/cam-hi.jpg'

# Load YOLO model
modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

# Read class names
classesfile = 'coco.names'
classNames = []
with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Initialize parameters
whT = 320
prev_frame = None

def detect_motion(current_frame, prev_frame):
    if prev_frame is None:
        return current_frame, False
    
    frame_diff = cv2.absdiff(current_frame, prev_frame)
    gray = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 5000:
            motion_detected = True
            cv2.drawContours(current_frame, [contour], -1, (0, 255, 0), 2)
            break
    return current_frame, motion_detected

# Function to play alert sound when an animal is detected
def play_alert_sound():
    winsound.PlaySound('alert.wav', winsound.SND_FILENAME)

def find_objects(outputs, img):
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
    
    if len(indices) > 0:
        indices = indices.flatten()
        for i in indices:
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            label = classNames[classIds[i]]
            confidence = int(confs[i] * 100)
            
            # Color based on confidence
            if confidence > 80:
                color = (0, 255, 0)  # Green for high confidence
            elif confidence > 60:
                color = (255, 255, 0)  # Yellow for medium confidence
            else:
                color = (0, 0, 255)  # Red for low confidence
            
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, f'{label.upper()} {confidence}%', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Play sound if an animal is detected (assuming 'dog' or 'cat' is in the class names)
            if label in ['dog', 'cat']:  # You can add more animal classes here
                play_alert_sound()
    
    return img

while True:
    try:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
    except urllib.error.URLError as e:
        print(f"Failed to connect to {url}: {e.reason}")
        continue
    
    blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
    net.setInput(blob)
    
    # Get output layer names
    layernames = net.getLayerNames()
    outputLayers = net.getUnconnectedOutLayers()
    
    # Adjust the outputLayers extraction
    if isinstance(outputLayers, list):
        outputNames = [layernames[i - 1] for i in outputLayers]
    else:
        outputNames = [layernames[i - 1] for i in outputLayers.flatten()]
    
    outputs = net.forward(outputNames)
    
    img, motion_detected = detect_motion(img, prev_frame)
    img = find_objects(outputs, img)
    
    if motion_detected:
        cv2.putText(img, 'Motion Detected!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    cv2.imshow('Detection', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
