import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model('models/isl_model.keras')

def predict_sign(image):
    prediction = model.predict(image)
    class_index = np.argmax(prediction, axis=1)
    return class_index[0]
