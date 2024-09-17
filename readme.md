---

# **ESP32-CAM Object Detection, Motion Detection, and WhatsApp Person Alert**
## **Overview**

This project integrates an ESP32-CAM with YOLOv3 to perform real-time object detection and motion detection. When a person is detected in the video stream, an image of the detected person is captured and sent via WhatsApp using `pywhatkit`. The system detects motion and highlights it on the live feed. It also displays the object class and confidence level for each detected object.

## **Features**

- **Real-time Object Detection**: Uses YOLOv3 to detect and classify objects in the video feed.
- **Motion Detection**: Highlights motion detected in the camera feed and shows a "Motion Detected" message.
- **Person Detection with WhatsApp Alert**: Sends an image via WhatsApp when a person is detected.
- **ESP32-CAM Integration**: Streams live video from the ESP32-CAM and processes it in real time.

## **Installation**

### **Python Code Setup**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/shashwatpandey29/Object-Detection.git
    ```

2. **Download YOLOv3 Weights and Config Files**:
   - Download the YOLOv3 weights from the [YOLO website](https://pjreddie.com/darknet/yolo/).
   - Download the YOLOv3 configuration file (`yolov3.cfg`).
   - Download the COCO class labels file (`coco.names`) from the [COCO dataset](https://cocodataset.org/#home).

   Place all the downloaded files (`yolov3.cfg`, `yolov3.weights`, `coco.names`) in the project directory.

3. **Install Required Python Libraries**:
    ```bash
    pip install opencv-python numpy pywhatkit
    ```

4. **Update the ESP32-CAM Feed URL**:
   - In the `main.py` file, update the `url` variable with the IP address of your ESP32-CAM.

   ```python
   url = 'http://192.168.98.8/cam-hi.jpg'  # Your ESP32-CAM IP address
   ```

5. **WhatsApp Integration**:
   - Replace the `whatsapp_number` in the Python code with your own WhatsApp number in international format (e.g., `+91XXXXXXXXXX` for India).

   ```python
   whatsapp_number = '+917007864516'  # Replace with your WhatsApp number in international format
   ```

## **Running the Project**

1. Run the Python script to start the object and motion detection:
    ```bash
    python main.py
    ```

2. The program will:
   - Stream live video from the ESP32-CAM.
   - Detect objects and highlight them with bounding boxes, displaying the confidence percentage.
   - Detect motion and show a "Motion Detected" message.
   - If a person is detected, it captures the image and sends it to your WhatsApp using `pywhatkit`.

3. To stop the program, press `q` while the video window is focused.

## **Notes**

- Ensure the ESP32-CAM is connected to the same network as the computer running the script.
- You must have WhatsApp Web logged in on your computer for the `pywhatkit` module to work. It will open a browser tab to send the image automatically.
- Make sure to update the `whatsapp_number` variable with your WhatsApp number in international format.

---
