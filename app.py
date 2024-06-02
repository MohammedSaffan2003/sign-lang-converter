from flask import Flask, render_template, request, jsonify
from src.predict import predict_sign
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files['file']
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        result = predict_sign(file_path)
        os.remove(file_path)
        return jsonify({'result': result})
    return jsonify({'error': 'No file uploaded'})

if __name__ == "__main__":
    app.run(debug=True)
