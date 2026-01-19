import os
import cv2
import torch
import numpy as np
from flask import Flask, render_template, request, Response, url_for

app = Flask(__name__)

# --- CONFIGURATION ---
# Path to your trained model (from your previous screenshot)
MODEL_PATH = r"yolov5/runs/train/yolov5s_results/weights/best.pt"
UPLOAD_FOLDER = 'static/uploads'

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Model
print("Loading YOLOv5 Model...")
try:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=MODEL_PATH, force_reload=True)
    model.conf = 0.5  # Confidence threshold
except Exception as e:
    print(f"Error loading model: {e}")
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
        
        # Run detection
        results = model(frame)
        
        # Render boxes on the frame
        annotated_frame = np.squeeze(results.render())
        
        # Encode frame to JPEG
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        # Stream the frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Home page"""
    # Close camera if it was open from a previous session
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
        # Save original file
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Run Inference
        results = model(filepath)
        
        # Save processed image
        results.save(save_dir=UPLOAD_FOLDER)
        
        # YOLO saves images in a specific way, we need to find the result
        # Usually it saves with the same name inside the save_dir
        # But for simplicity, let's just overwrite or find the file
        # YOLO .save() creates a folder, let's just render the array manually to keep it simple
        
        annotated_img = np.squeeze(results.render())
        result_path = os.path.join(UPLOAD_FOLDER, 'pred_' + file.filename)
        cv2.imwrite(result_path, cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))

        return render_template('index.html', image_path=result_path)

@app.route('/video_feed')
def video_feed():
    """Route for the live video feed"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    print("Starting Web App...")
    app.run(debug=True, port=5000)