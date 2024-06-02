from flask import Flask, render_template, request, jsonify
from src.predict import predict_sign
import base64
import cv2
import numpy as np
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data'}), 400

    image_data = data['image']
    image_data = image_data.split(',')[1]  # Remove data:image/png;base64, prefix
    image_bytes = base64.b64decode(image_data)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = predict_sign(img)

    return jsonify({'result': result})

if __name__ == "__main__":
    app.run(debug=True)
