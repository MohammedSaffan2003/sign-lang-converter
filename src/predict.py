import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import numpy as np

model = load_model('models/isl_model.h5')

def predict_sign(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64))
    img = img.reshape(1, 64, 64, 1)
    img = img / 255.0
    prediction = model.predict(img)
    class_index = np.argmax(prediction, axis=1)
    return class_index[0]
