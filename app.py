from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import tensorflow as tf
import base64
import re
import mediapipe as mp

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('models/isl_model.keras')

# Define the mapping from numerical predictions to sign language letters
label_mapping = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
    5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e',
    15: 'f', 16: 'g', 17: 'h', 18: 'i', 19: 'j',
    20: 'k', 21: 'l', 22: 'm', 23: 'n', 24: 'o',
    25: 'p', 26: 'q', 27: 'r', 28: 's', 29: 't',
    30: 'u', 31: 'v', 32: 'w', 33: 'x', 34: 'y',
    35: 'z'
}

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']
    
    if 'data:image' in image_data:
        image_data = re.sub('^data:image/.+;base64,', '', image_data)

    img_bytes = base64.b64decode(image_data)
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5) as hands:
        results = hands.process(img)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = img.shape
            x_min, x_max, y_min, y_max = w, 0, h, 0
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                x_min, x_max = min(x_min, x), max(x_max, x)
                y_min, y_max = min(y_min, y), max(y_max, y)

            hand_img = img[y_min:y_max, x_min:x_max]
            hand_img = cv2.cvtColor(hand_img, cv2.COLOR_RGB2GRAY)
            hand_img = cv2.resize(hand_img, (64, 64))
            hand_img = hand_img.reshape(1, 64, 64, 1)
            hand_img = hand_img / 255.0

            prediction = model.predict(hand_img)
            predicted_class = np.argmax(prediction)
            sign_language_letter = label_mapping[predicted_class]
        else:
            sign_language_letter = "No hand detected"

    response = {'prediction': sign_language_letter}
    return jsonify(response)

@app.route('/predict_upload', methods=['POST'])
def predict_upload():
    data = request.get_json()
    image_data = data['image']

    img_bytes = base64.b64decode(image_data)
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (64, 64))
    img = img.reshape(1, 64, 64, 1)
    img = img / 255.0

    prediction = model.predict(img)
    predicted_class = np.argmax(prediction)
    sign_language_letter = label_mapping[predicted_class]

    response = {'prediction': sign_language_letter}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
