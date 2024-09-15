# **ESP32-CAM Object Detection and Motion Detection**

## **Overview**

This project involves using an ESP32-CAM and YOLOv3 for real-time object detection and motion detection. It captures live video from the ESP32-CAM, processes it to detect objects, and highlights any motion. The project displays detected objects with their confidence levels and indicates when motion is detected.

## **Features**

- **Real-time Object Detection**: Identifies objects in the video stream using YOLOv3.
- **Motion Detection**: Detects motion and highlights it in the video feed.
- **Dynamic Labeling**: Displays class names and confidence levels for detected objects.
- **ESP32-CAM Integration**: Streams video from the ESP32-CAM.

## **Installation**

### **Python Code for Object Detection**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/esp32-object-detection.git
    cd esp32-object-detection
    ```

2. **Download YOLOv3 Weights and Config Files**:
   - Download the YOLOv3 weights from the [YOLO website](https://pjreddie.com/darknet/yolo/).
   - Download the YOLOv3 configuration file (`yolov3.cfg`).
   - Download the COCO class labels file (`coco.names`) from the [COCO dataset](https://cocodataset.org/#home).

   Place these files in the project directory.

3. **Install Python Dependencies**:
    ```bash
    pip install opencv-python numpy
    ```

4. **Update ESP32-CAM Feed URL**:
   - Open `main.py` and update the `url` variable with the IP address of your ESP32-CAM.

   ```python
   url = 'http://192.168.98.8/cam-hi.jpg'

