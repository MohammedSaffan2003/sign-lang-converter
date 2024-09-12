# Hand Gesture Recognition

Hand Gesture Recognition is a project designed to translate sign language gestures into text and images, particularly focusing on Indian Sign Language (ISL). This project includes features such as real-time hand gesture recognition, text to sign language conversion, and text-to-sign image retrieval.

## Features

- **Predict Upload**: Upload an image of a hand gesture to predict the corresponding sign language character.
- **Text to Sign Language Conversion**: Converts a text input into sign language, showing the corresponding hand gestures.
- **General Sign Language Recognition**: Utilizes a webcam feed to recognize and predict general signs in real time.
- **Text to Sign Image Retrieval**: Converts text phrases into corresponding sign language gesture images.

## Technology Stack

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: TensorFlow, Keras
- **Computer Vision**: OpenCV, MediaPipe
- **Image Handling**: PIL (Python Imaging Library)
- **Data**: Indian Sign Language Dataset from Kaggle

## Dataset

The dataset used for training consists of Indian Sign Language (ISL) alphabet and numbers, provided by ISRTC (Indian Sign Research and Training Center). The dataset includes black and white images for efficient computing and better accuracy during training.

- Dataset link: [ISL Dataset on Kaggle](https://www.kaggle.com/datasets/kshitij192/isl-dataset)

## Functionalities

- **Upload Image Prediction**: Upload an image of a hand gesture and get the predicted sign language character.
- **Real-time Gesture Recognition**: Detects and identifies hand gestures in real-time through webcam feed.
- **Text to Sign Language**: Convert any text input into its corresponding sign language gestures.
- **Sign Language Image Retrieval**: Retrieves images of signs based on text input.

## System Architecture

1. User uploads an image or provides text input.
2. The image is processed using OpenCV and MediaPipe to detect the hand gesture.
3. The machine learning model (trained on the ISL dataset) predicts the corresponding sign.
4. For text input, each word is converted into corresponding sign language gestures.
5. The results are displayed either as text, real-time video predictions, or images.
