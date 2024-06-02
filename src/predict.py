import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import cv2

model = load_model('models/isl_model.keras')  # Ensure the model path is correct

def predict_sign(img):
    if len(img.shape) == 3:  # if the image is colored (3 channels), convert to grayscale
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (64, 64))
    img = img.reshape(1, 64, 64, 1)
    img = img / 255.0
    prediction = model.predict(img)
    class_index = np.argmax(prediction, axis=1)
    return int(class_index[0])
