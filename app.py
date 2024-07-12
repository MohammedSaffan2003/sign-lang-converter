# app.py
from flask import Flask, request, jsonify, render_template,send_file
import cv2
import numpy as np
import tensorflow as tf
import base64
import re
import mediapipe as mp
import os
import io
import os
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from gesture_detection import detect_hand_gesture
# Load communication dictionary
from communication_dict import communication_dict

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

# for general sign feature 
mp_hands = mp.solutions.hands

@app.route('/general_sign_predict', methods=['POST'])
def general_sign_predict():
    data = request.get_json()
    image_data = data['image']
    
    if 'data:image' in image_data:
        image_data = re.sub('^data:image/.+;base64,', '', image_data)

    img_bytes = base64.b64decode(image_data)
    img_np = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    gesture, frame = detect_hand_gesture(img)
    
    if gesture in communication_dict:
        response_text = communication_dict[gesture]
    else:
        response_text = "Unknown Gesture"

    response = {'prediction': response_text}
    return jsonify(response)

# for text-image feature
def fetch_image_from_web(phrase):
    query = phrase.replace("_", "+")
    url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:photo-photo"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_results = soup.find_all('img', class_='mimg')

    if image_results:
        image_url = image_results[0]['src']
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            return image_response.content
    return None

@app.route('/text_to_image', methods=['POST'])
def text_to_image():
    data = request.get_json()
    phrase = data['phrase'].strip().lower().replace(" ", "_")  # Normalize the phrase

    # Define the directory where your stored images are located
    images_dir = 'stored_images'
    image_path = os.path.join(images_dir, f"{phrase}.png")

    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/png')
    else:
        web_image = fetch_image_from_web(phrase)
        if web_image:
            return send_file(
                io.BytesIO(web_image),
                mimetype='image/png',
                as_attachment=True,
                attachment_filename=f"{phrase}.png"
            )
        else:
            return jsonify({'error': 'Image not found'}), 404
# def fetch_image_from_web(phrase):
#     search_url = "https://api.example.com/search"
#     params = {"query": phrase}
#     response = requests.get(search_url, params=params)
    
#     if response.status_code == 200:
#         image_url = response.json()['image_url']
#         image_response = requests.get(image_url)
#         return Image.open(BytesIO(image_response.content))
#     else:
#         return None

# @app.route('/text_to_image', methods=['POST'])
# def text_to_image():
#     data = request.get_json()
#     phrase = data.get('phrase')
    
#     if not phrase:
#         return jsonify({'error': 'Phrase is required'}), 400
    
#     # Check if the image is stored locally
#     image_path = f"stored_images/{phrase}.jpg"
    
#     if os.path.exists(image_path):
#         return send_file(image_path, mimetype='image/jpeg')
#     else:
#         # Fetch image from the web
#         image = fetch_image_from_web(phrase)
#         if image:
#             image.save(image_path)
#             return send_file(image_path, mimetype='image/jpeg')
#         else:
#             return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(port=5000)
