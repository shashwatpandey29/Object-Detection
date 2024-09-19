from flask import Flask, render_template, Response
import cv2
import numpy as np
import urllib.request
import time
import matplotlib.pyplot as plt

# Flask app setup
app = Flask(__name__)

# YOLO and Motion Detection Setup
url = 'http://192.168.244.8/cam-hi.jpg'
modelConfig = 'yolov3.cfg'
modelWeights = 'yolov3.weights'
net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL)

# Load YOLO class names
classesfile = 'coco.names'
classNames = []
with open(classesfile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Initialize variables
whT = 320
prev_frame = None
motion_counter = 0
detection_counter = 0

# Motion detection
def detect_motion(current_frame, prev_frame):
    global motion_counter
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
            motion_counter += 1
            cv2.drawContours(current_frame, [contour], -1, (0, 255, 0), 2)
            break
    return current_frame, motion_detected

# Object detection with YOLO
def find_objects(outputs, img):
    global detection_counter
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
                detection_counter += 1
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
    
    return img

# Frame generator for live streaming
def generate_frames():
    global prev_frame
    while True:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
        
        blob = cv2.dnn.blobFromImage(img, 1 / 255, (whT, whT), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        
        layernames = net.getLayerNames()
        outputLayers = net.getUnconnectedOutLayers()
        outputNames = [layernames[i - 1] for i in outputLayers.flatten()]
        outputs = net.forward(outputNames)
        
        img, motion_detected = detect_motion(img, prev_frame)
        img = find_objects(outputs, img)
        prev_frame = img
        
        if motion_detected:
            cv2.putText(img, 'Motion Detected!', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    global motion_counter, detection_counter
    plt.figure(figsize=(5, 5))
    labels = ['Motions Detected', 'Objects Detected']
    sizes = [motion_counter, detection_counter]
    colors = ['skyblue', 'lightgreen']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.savefig('static/analytics.png')
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(debug=True)
