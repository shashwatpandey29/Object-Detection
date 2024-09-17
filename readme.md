Here's a README file for the code you provided, based on the previous structure:

---

# ESP32-CAM Object Detection and Motion Detection System

This project leverages an ESP32-CAM module to capture real-time video feed and perform object detection and motion detection using the YOLOv3 algorithm. The system is designed to detect motion in the video feed and highlight objects, especially if a person is detected. It uses OpenCV for image processing and computer vision tasks.

## Features

- **Real-time Object Detection**: Uses YOLOv3 for object detection, identifying multiple objects such as people, cars, etc.
- **Motion Detection**: Identifies movement in the video feed by comparing frames.
- **Configurable Model**: The system allows easy switching between CPU and GPU for performance tuning.
- **Dynamic Display**: The detected objects are highlighted with bounding boxes, and the detection window is resizable for better viewing.
- **Confidence-based Coloring**: Detected objects are highlighted in different colors depending on the confidence level of detection.
- **Efficient Processing**: Frames are resized and optimized to reduce processing time and lag.

## Requirements

- **ESP32-CAM**: Set up and streaming on your local network (default URL `http://192.168.98.8/cam-hi.jpg`).
- **YOLOv3**: Pre-trained YOLOv3 model, including `yolov3.cfg` and `yolov3.weights`.
- **OpenCV**: The project utilizes OpenCV for image processing and blob creation.
- **Python 3.x**: Ensure Python is installed on your system with the necessary libraries.
  
## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/esp32-cam-object-detection.git
    ```

2. Install the required dependencies:
    ```bash
    pip install opencv-python numpy urllib3
    ```

3. Download the YOLOv3 pre-trained weights and configuration files:
    - `yolov3.weights`: [Download here](https://pjreddie.com/media/files/yolov3.weights)
    - `yolov3.cfg`: [Download here](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
    - `coco.names`: This file contains the names of the classes YOLOv3 detects, and can be downloaded [here](https://github.com/pjreddie/darknet/blob/master/data/coco.names).

4. Place these files in the project directory.

## Usage

1. Connect your ESP32-CAM to the same network as your computer and obtain its stream URL (default is `http://192.168.98.8/cam-hi.jpg`).

2. Run the detection script:
    ```bash
    python detect.py
    ```

3. Adjust configurations in the code:
   - **Model Configurations**: If you want to switch to GPU, modify the following line:
     ```python
     net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)  # For GPU use
     ```
   - **Motion Detection Sensitivity**: You can adjust the contour area threshold for detecting motion by modifying the area in the `detect_motion` function:
     ```python
     if cv2.contourArea(contour) > 5000:
     ```

4. The system will open a real-time display window showing detected objects and motion. If motion is detected, the label "Motion Detected!" will appear on the screen.

## Configuration

- **Frame Skipping**: Adjust the `frame_skip` variable to skip frames between object detection to increase processing speed.
  ```python
  frame_skip = 2
  ```

- **Confidence Threshold**: Modify the detection confidence threshold by adjusting this line in the code:
  ```python
  if confidence > 0.5:
  ```

- **Scaling Factor**: Change the scaling factor to adjust the size of the display window.
  ```python
  scale_factor = 2.0  # For doubling the display size
  ```

## Output

- Bounding boxes around detected objects with labels showing the class name and confidence level.
- Motion detection alerts with a "Motion Detected!" message.
- The detection window can be resized, and the program can be stopped by pressing the 'q' key.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

