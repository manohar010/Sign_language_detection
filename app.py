from flask import Flask, render_template, Response
import cv2
import torch
import os

app = Flask(__name__)

# --- WRITE YOUR PATH HERE ---
# Use the 'r' prefix to handle Windows backslashes correctly
model_path = r"D:\bappy\office\Recordings\code\Sign_language_detection\artifacts\12_28_2025_14_14_50\model_trainer\best.pt"

# Load the model using the path defined above
# We add trust_repo=True to bypass the security warning you saw earlier
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True, trust_repo=True)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame)
            results.render()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)