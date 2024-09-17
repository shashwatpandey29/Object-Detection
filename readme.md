Here's a README.md for your updated program:

```markdown
# **ESP32-CAM Object Detection with Animal Alert**

## **Overview**

This project uses an ESP32-CAM with YOLOv3 for real-time object detection and motion detection. It captures live video from the ESP32-CAM, processes the video feed to detect objects, highlights any motion, and plays an alert sound when animals such as dogs or cats are detected.

## **Features**

- **Real-time Object Detection**: Identifies objects in the video stream using the YOLOv3 model.
- **Motion Detection**: Detects motion in the video feed and highlights it.
- **Animal Detection Alert**: Plays an audio alert when animals (e.g., dogs, cats) are detected.
- **Error Handling**: Includes error handling for connection issues with the ESP32-CAM feed.

## **Installation**

### **Python Code for Object Detection and Alert**

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/shashwatpandey29/Object-Detection.git
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

4. **Prepare the Audio Alert**:
   - Ensure you have an audio file named `alert.wav` in the project directory. This file will be played when an animal is detected.

5. **Update ESP32-CAM Feed URL**:
   - Open `main.py` and update the `url` variable with the URL of your ESP32-CAM.

   ```python
   url = 'http://your_esp32_cam_ip/cam-hi.jpg'
   ```

## **Usage**

1. **Run the Program**:
    ```bash
    python main.py
    ```

2. **Program Behavior**:
   - The program continuously captures frames from the ESP32-CAM feed.
   - It processes each frame to detect objects and motion.
   - If an animal (e.g., dog, cat) is detected, an alert sound is played.
   - Motion detection results and object classifications are displayed in real-time.

3. **Stopping the Program**:
   - To stop the program, press `q` while the video window is focused.

## **Troubleshooting**

- **Connection Errors**: Ensure the ESP32-CAM is properly connected and the URL is correct.
- **Audio Alert Issues**: Verify that the `alert.wav` file is in the correct location and is accessible.

## **Contributing**

Feel free to submit issues or pull requests if you have suggestions or improvements.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```
