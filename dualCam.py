import cv2
import torch
import numpy as np
import time

# Load YOLOv7 model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = torch.hub.load('WongKinYiu/yolov7', 'custom', path_or_model='yolov7.pt', force_reload=True).to(device)

# Initialize dual cameras (e.g., camera 0 and 1)
cap1 = cv2.VideoCapture(0)  # First camera
cap2 = cv2.VideoCapture(1)  # Second camera

# Check if cameras opened successfully
if not (cap1.isOpened() and cap2.isOpened()):
    print("Error: Could not open one or both cameras.")
    exit()

# Set the resolution for both cameras
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Detection settings
conf_threshold = 0.25  # Confidence threshold for object detection

while True:
    # Capture frame-by-frame from both cameras
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not (ret1 and ret2):
        print("Error: Failed to capture frames.")
        break

    # Prepare the frames for YOLO
    frames = [frame1, frame2]

    for idx, frame in enumerate(frames):
        # Convert frame to RGB (YOLOv7 model expects RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert the frame into a tensor and scale
        img = torch.from_numpy(rgb_frame).permute(2, 0, 1).float().to(device)
        img = img.unsqueeze(0) / 255.0

        # Inference
        with torch.no_grad():
            pred = model(img)[0]

        # Apply confidence threshold and NMS (Non-Maximum Suppression)
        pred = pred[pred[:, 4] > conf_threshold]
        pred = pred.cpu().numpy()

        # Draw bounding boxes and labels on the frame
        for det in pred:
            x1, y1, x2, y2, conf, cls = map(int, det[:6])
            label = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Show the resulting frame with detections
        cv2.imshow(f'Camera {idx+1}', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera resources and close windows
frame1.release()
frame2.release()
cv2.destroyAllWindows()
       
