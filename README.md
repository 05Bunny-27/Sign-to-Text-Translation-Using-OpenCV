

# Sign-to-Text Language Translator for Indian Sign Language (ISL)

## Overview
This project aims to develop a real-time **Sign-to-Text Language Translator** specifically designed for **Indian Sign Language (ISL)**. By utilizing **OpenCV**, **computer vision**, and **neural networks**, the system bridges communication gaps for the deaf-mute community by translating ISL gestures into text and voice outputs. 

## Features
- **Real-Time Gesture Recognition**: Powered by a Convolutional Neural Network (CNN) for accurate and efficient ISL gesture interpretation.
- **Custom Dataset Creation**: Generates datasets using OpenCV for high-quality training and testing.
- **Finger Spelling**: Supports sentence formation through finger spelling gestures.
- **Text-to-Speech**: Converts recognized gestures into spoken words for enhanced usability.
- **User-Friendly Output**: Displays interpreted gestures as sentences on-screen and vocalizes them.
- **Suggestions and Corrections**: Offers recommendations to form grammatically correct sentences.

## Technology Stack
- **Programming Language**: Python
- **Libraries**:
  - OpenCV
  - TensorFlow/Keras
  - NumPy
  - Matplotlib
  - Pyttsx3 (for text-to-speech)
- **Machine Learning Models**: Convolutional Neural Networks (CNN)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/sign-to-text-translator.git
   cd sign-to-text-translator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Dataset Preparation
1. Capture gesture images using the built-in OpenCV-based data collection tool.
2. Preprocess the images by resizing and normalizing them.
3. Train the CNN model with the custom dataset.

## Usage
1. Start the application and position your hand in front of the camera.
2. Perform gestures corresponding to ISL alphabets or words.
3. View the interpreted text on the screen.
4. Listen to the text converted into speech for real-time communication.

## Contribution
We welcome contributions to improve the system! Here's how you can contribute:
1. Fork the repository.
2. Create a new branch for your feature/bug fix.
3. Commit your changes and push them to your branch.
4. Create a pull request explaining your changes.


## Acknowledgments
- Special thanks to the developers and researchers advancing gesture recognition technologies.
- Inspired by the need for inclusive communication tools for the deaf-mute community.

---

Let me know if you'd like any modifications!
