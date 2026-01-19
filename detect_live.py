import cv2
import torch
import numpy as np

# 1. Load your newly trained model
# The path is based on your screenshot log: "runs\train\yolov5s_results\weights\best.pt"
model_path = r"yolov5/runs/train/yolov5s_results/weights/best.pt"

print(f"Loading model from: {model_path}")

try:
    # Load the model using torch hub
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)
    
    # Set confidence threshold (only show detections if > 40% sure)
    model.conf = 0.4  
except Exception as e:
    print(f"Error loading model: {e}")
    exit()

# 2. Open Camera
cap = cv2.VideoCapture(0)

print("Starting Camera... Press 'q' to exit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Make Detections
    results = model(frame)
    
    # 4. Draw the box on the frame
    # np.squeeze removes extra dimensions to make it a valid image for OpenCV
    cv2.imshow('Sign Language Detection', np.squeeze(results.render()))
    
    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()