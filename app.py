from flask import Flask, render_template, request, jsonify
from src.predict import predict_sign
import os
import cv2
import numpy as np
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.json:
        return jsonify({'error': 'No image data'}), 400

    image_data = request.json['image']
    image_data = image_data.split(",")[1]
    image_data = base64.b64decode(image_data)

    # Ensure the uploads directory exists
    os.makedirs('uploads', exist_ok=True)

    file_path = 'uploads/captured_image.png'
    with open(file_path, "wb") as fh:
        fh.write(image_data)

    # Preprocess the image for prediction
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.flip(img, 1)  # Flip image horizontally
    img = cv2.resize(img, (64, 64))
    img = img.reshape(1, 64, 64, 1) / 255.0

    # Predict the sign
    result = predict_sign(img)
    os.remove(file_path)
    return jsonify({'result': str(result)})

if __name__ == "__main__":
    app.run(debug=True)
