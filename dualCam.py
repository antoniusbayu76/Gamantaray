import cv2
import torch
import numpy as np
from pathlib import Path

# Add the YOLOv7 directory to the system path
import sys
sys.path.insert(0, 'path_to_yolov7_repo')  # Replace with your actual path

# Import YOLOv7-specific functions
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.torch_utils import select_device

# Load YOLOv7 model
model_path = 'yolov7.pt'  # Path to your YOLOv7 weights
device = select_device('')
model = attempt_load(model_path, map_location=device)
model.eval()

# Initialize dual camera capture
camera1 = cv2.VideoCapture(0)  # First camera
camera2 = cv2.VideoCapture(1)  # Second camera

# Set frame width and height if necessary
camera1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def process_frame(frame):
    """ Process a frame through YOLOv7 model for object detection """
    # Prepare the image
    img = letterbox(frame, new_shape=640)[0]
    img = img.transpose((2, 0, 1))[::-1]
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device).float() / 255.0
    img = img.unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        pred = model(img)[0]
    
    # Apply NMS
    pred = non_max_suppression(pred, conf_thres=0.4, iou_thres=0.5)
    return pred

while True:
    # Capture frame-by-frame from both cameras
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    if not ret1 or not ret2:
        print("Failed to grab frames from one or both cameras.")
        break

    # Run object detection on both frames
    results1 = process_frame(frame1)
    results2 = process_frame(frame2)

    # Convert the results to OpenCV-compatible format and display detections
    def draw_results(frame, results):
        for det in results[0]:
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], frame.shape).round()
                for *xyxy, conf, cls in det:
                    label = f'{model.names[int(cls)]}: {conf:.2f}'
                    x1, y1, x2, y2 = map(int, xyxy)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    draw_results(frame1, results1)
    draw_results(frame2, results2)

    # Display the resulting frames
    combined_frame = np.hstack((frame1, frame2))
    cv2.imshow('Dual Camera Object Detection', combined_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources and close windows
camera1.release()
camera2.release()
cv2.destroyAllWindows()
