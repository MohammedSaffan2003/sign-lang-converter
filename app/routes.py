from flask import request, jsonify, render_template
import base64
import re
import cv2
import numpy as np
from .model import load_model, label_mapping

model = load_model()

def init_app(app):
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
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (64, 64))
        img = img.reshape(1, 64, 64, 1) / 255.0

        prediction = model.predict(img)
        predicted_class = np.argmax(prediction)
        sign_language_letter = label_mapping[predicted_class]

        response = {'prediction': sign_language_letter}
        return jsonify(response)
