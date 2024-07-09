from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import tensorflow as tf
import base64
import re

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    image_data = data['image']
    
    if 'data:image' in image_data:
        # Base64 string with header, remove the header part
        image_data = re.sub('^data:image/.+;base64,', '', image_data)

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
