import cv2
from ultralytics import YOLO

# 1. Load your newly trained YOLOv8 model
# UPDATED PATH: YOLOv8 saves typically in 'runs/detect/...'
# Check your folder to confirm if it is 'train' or 'detect'
model_path = r"runs/detect/yolov8_results/weights/best.pt"

print(f"Loading YOLOv8 model from: {model_path}")

try:
    # Load the model using the ultralytics library
    model = YOLO(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    print("Double check that the path to best.pt is correct!")
    exit()

# 2. Open Camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting Camera... Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # 3. Make Detections
    # conf=0.4 sets the confidence threshold to 40%
    results = model(frame, conf=0.4)
    
    # 4. Draw the box on the frame
    # YOLOv8: results[0].plot() returns the image as a numpy array directly
    annotated_frame = results[0].plot()

    # Display the resulting frame
    cv2.imshow('Sign Language Detection (YOLOv8)', annotated_frame)
    
    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()