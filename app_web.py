import os
import cv2
import time
import pyttsx3
from collections import deque
from flask import Flask, render_template, request, Response, jsonify
from ultralytics import YOLO

app = Flask(__name__)

# -------- CONFIG -------- #
MODEL_PATH = "runs/detect/yolo11_results/weights/best.pt"

UPLOAD_FOLDER = 'static/uploads'
PREDICT_FOLDER = 'static/predictions'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PREDICT_FOLDER, exist_ok=True)

# Load model
model = YOLO(MODEL_PATH)

# Text-to-Speech
engine = pyttsx3.init()

# -------- GLOBAL VARIABLES -------- #
camera = None
letter_buffer = deque(maxlen=15)

current_word = ""
last_spoken = ""

last_letter = "-"
last_confidence = 0.0

# Tracks the last signed word to prevent spamming
last_appended_sign = ""


# -------- SPEAK -------- #
def speak(text):
    global last_spoken
    if text and text != last_spoken:
        engine.say(text)
        engine.runAndWait()
        last_spoken = text


# -------- STABLE LETTER -------- #
def get_stable_letter():
    if len(letter_buffer) < 10:
        return None

    most_common = max(set(letter_buffer), key=letter_buffer.count)

    if letter_buffer.count(most_common) > 7:
        return most_common
    return None


# -------- VIDEO STREAM -------- #
def generate_frames():
    global camera, current_word, last_letter, last_confidence, last_appended_sign

    camera = cv2.VideoCapture(0)
    prev_time = 0

    while True:
        if camera is None or not camera.isOpened():
            break

        success, frame = camera.read()
        if not success:
            break

        results = model(frame)
        annotated = results[0].plot()

        detected_letter = None
        confidence = 0.0

        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            detected_letter = model.names[cls_id]

        if detected_letter:
            letter_buffer.append(detected_letter)
            last_letter = detected_letter
            last_confidence = round(confidence, 2)

        stable_letter = get_stable_letter()

        # Logic to check against whole words and add spaces (Fixes repeating issue)
        if stable_letter:
            if stable_letter != last_appended_sign:
                if stable_letter == "SPACE":
                    speak(current_word)
                    current_word = ""
                else:
                    if current_word == "":
                        current_word += stable_letter
                    else:
                        current_word += " " + stable_letter
                
                # Lock out this word until a new sign is detected
                last_appended_sign = stable_letter

        # FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time

        # Overlay
        cv2.putText(annotated, f"Letter: {stable_letter}",
                    (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(annotated, f"Word: {current_word}",
                    (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        cv2.putText(annotated, f"Conf: {last_confidence}",
                    (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.putText(annotated, f"FPS: {int(fps)}",
                    (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', annotated)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    if camera:
        camera.release()
        camera = None


# -------- ROUTES -------- #

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    global current_word, last_letter, last_confidence

    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    results = model(filepath)
    annotated_img = results[0].plot()

    if len(results[0].boxes) > 0:
        box = results[0].boxes[0]
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        last_letter = model.names[cls_id]
        last_confidence = round(conf, 2)

        if current_word == "":
            current_word += last_letter
        else:
            current_word += " " + last_letter

    output_filename = "pred_" + file.filename
    output_path = os.path.join(PREDICT_FOLDER, output_filename)

    cv2.imwrite(output_path, annotated_img)

    # FIX: Pass prediction data to the HTML template so it shows up after uploading
    return render_template('index.html',
                           image_path=f"static/predictions/{output_filename}",
                           pred_letter=last_letter,
                           pred_word=current_word,
                           pred_conf=last_confidence)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stop_camera')
def stop_camera():
    global camera
    if camera:
        camera.release()
        camera = None
    return jsonify({"status": "stopped"})


@app.route('/clear_word')
def clear_word():
    global current_word, last_appended_sign
    current_word = ""
    last_appended_sign = ""
    return jsonify({"status": "cleared"})


@app.route('/get_word')
def get_word():
    return jsonify({"word": current_word})


@app.route('/get_stats')
def get_stats():
    return jsonify({
        "letter": last_letter,
        "confidence": last_confidence
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)