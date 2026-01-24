import os
import cv2
import numpy as np
from flask import Flask, render_template, request, Response
from ultralytics import YOLO  # <--- UPDATED for YOLOv8

app = Flask(__name__)

# --- CONFIGURATION ---
# Path to your YOLOv8 trained model
# Based on your previous logs, it should be here:
MODEL_PATH = r"runs/detect/yolov8_results/weights/best.pt"

# Folder configuration
UPLOAD_FOLDER = 'static/uploads'
PREDICT_FOLDER = 'static/predictions'

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICT_FOLDER, exist_ok=True)

# Load Model
print(f"Loading YOLOv8 Model from {MODEL_PATH}...")
try:
    model = YOLO(MODEL_PATH)  # <--- Load YOLOv8 model
except Exception as e:
    print(f"Error loading model: {e}")
    print("Please verify the path to your 'best.pt' file.")
    exit()

# Global camera variable
camera = None

def generate_frames():
    """Generator function for live video streaming"""
    global camera
    camera = cv2.VideoCapture(0)  # Open webcam
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Run detection (YOLOv8)
        # stream=True is more efficient for video generators
        results = model(frame, stream=True)
        
        for result in results:
            # Plot the results on the frame
            # YOLOv8 returns BGR by default, perfect for OpenCV
            annotated_frame = result.plot()
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            frame_bytes = buffer.tobytes()
            
            # Stream the frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    # Release camera when loop breaks (though usually this loop runs forever)
    if camera:
        camera.release()

@app.route('/')
def index():
    """Home page"""
    # Force close camera if it was open to free up resource
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle Image Upload and Prediction"""
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    if file:
        # 1. Save original file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 2. Run Inference
        results = model(filepath)
        
        # 3. Process Result
        # results[0].plot() returns the image as a numpy array (BGR)
        annotated_img = results[0].plot()
        
        # 4. Save processed image to 'static/predictions' so HTML can see it
        output_filename = 'pred_' + file.filename
        output_path = os.path.join(PREDICT_FOLDER, output_filename)
        
        cv2.imwrite(output_path, annotated_img)

        # 5. Return template with the new image path
        # Note: In HTML, path should be relative to 'static' or root, not absolute system path
        web_image_path = f"static/predictions/{output_filename}"
        
        return render_template('index.html', image_path=web_image_path)

@app.route('/video_feed')
def video_feed():
    """Route for the live video feed"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("Starting Web App...")
    # host='0.0.0.0' allows access from other devices on the same network
    app.run(host='0.0.0.0', port=5000, debug=True)