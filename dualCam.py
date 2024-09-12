import cv2
import torch
import numpy as np
from yolov7.models.experimental import attempt_load
from yolov7.utils.general import non_max_suppression, scale_coords
from yolov7.utils.datasets import letterbox
from yolov7.utils.torch_utils import select_device

# Load YOLOv7 model
def load_yolov7_model(weights_path, device):
    model = attempt_load(weights_path, map_location=device)  # Load model
    model.eval()  # Set model to evaluation mode
    return model

# Preprocess frame for YOLOv7 input
def preprocess_frame(frame, img_size=640):
    img = letterbox(frame, img_size, stride=32)[0]  # Resize while maintaining aspect ratio
    img = img[:, :, ::-1].transpose(2, 0, 1)  # Convert BGR to RGB, shape (3,640,640)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device).float() / 255.0  # Normalize to [0,1]
    if img.ndimension() == 3:
        img = img.unsqueeze(0)  # Add batch dimension
    return img

# Perform object detection
def detect_objects(model, img, conf_thres=0.25, iou_thres=0.45):
    with torch.no_grad():
        pred = model(img, augment=False)[0]  # Forward pass through YOLOv7
        pred = non_max_suppression(pred, conf_thres, iou_thres)  # Apply NMS to filter results
    return pred

# Post-process detections for visualization
def process_detections(pred, frame, img_size):
    for det in pred:  # detections per image
        if len(det):
            det[:, :4] = scale_coords(img_size, det[:, :4], frame.shape).round()
            for *xyxy, conf, cls in det:
                label = f'{conf:.2f}'
                cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(xyxy[0]), int(xyxy[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

# Main function to run dual camera object detection
def run_dual_camera_detection(weights='yolov7.pt', img_size=640):
    # Select device
    device = select_device('')
    
    # Load model
    model = load_yolov7_model(weights, device)
    
    # Open two cameras
    cam1 = cv2.VideoCapture(0)
    cam2 = cv2.VideoCapture(1)
    
    if not cam1.isOpened() or not cam2.isOpened():
        print("Error: Unable to access cameras")
        return
    
    while cam1.isOpened() and cam2.isOpened():
        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()

        if not ret1 or not ret2:
            print("Error: Unable to read frames from cameras")
            break
        
        # Preprocess frames
        img1 = preprocess_frame(frame1, img_size)
        img2 = preprocess_frame(frame2, img_size)

        # Detect objects in both frames
        pred1 = detect_objects(model, img1)
        pred2 = detect_objects(model, img2)

        # Process detections and visualize results
        frame1 = process_detections(pred1, frame1, img_size)
        frame2 = process_detections(pred2, frame2, img_size)

        # Display both frames
        cv2.imshow("Camera 1", frame1)
        cv2.imshow("Camera 2", frame2)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release cameras and close windows
    cam1.release()
    cam2.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_dual_camera_detection()
