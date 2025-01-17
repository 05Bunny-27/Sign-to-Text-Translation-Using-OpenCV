import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="SymbolDatabase.GetPrototype() is deprecated")

import pickle
import cv2
import mediapipe as mp
import numpy as np
import tkinter as tk
import threading
import time
import logging
import pyttsx3  # For text-to-speech
from PIL import Image, ImageTk, ImageSequence  # For displaying GIFs

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize the text-to-speech engine
engine = pyttsx3.init()




# Function to set voice gender
def set_voice_gender(gender):
    voices = engine.getProperty('voices')
    if gender == 'Male':
        engine.setProperty('voice', voices[0].id)  # Typically male voice
    elif gender == 'Female':
        engine.setProperty('voice', voices[1].id)  # Typically female voice

# Default to male voice
set_voice_gender('Male')

# Load the model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Mediapipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.7, max_num_hands=1)

# Labels dictionary
labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
    6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
    12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
    18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
    24: 'Y', 25: 'Z', 26: '0', 27: '1', 28: '2',
    29: '3', 30: '4', 31: '5', 32: '6', 33: '7', 34: '8', 35: '9',
    36: 'I love You', 37: 'yes', 38: 'No', 39: 'Hello', 40: 'Thanks',
    41: 'Sorry', 43: 'space'
}

# Gesture suggestions dictionary
suggestions_dict = {
    "A": "Apple Ant Apricot",
    "B": "Ball Bat Boy Bikshapathi",
    "C": "Cow Cap Cat",
    "H": " Horse.",
    "I": " Ice Cream.",
    "J": " Jelly.",
    "K": " Kite.",
    "L": " Lion.",
    "M": " Monkey.",
    "N": " Nest.",
    "O": " Owl.",
    "P": " Penguin.",
    "Q": " Queen.",
    "R": " Rabbit.",
    "S": " Snake.",
    "T": " Tiger.",
    "U": " Umbrella.",
    "V": " Violin.",
    "W": " Whale.",
    "X": " Xylophone.",
    "Y": " Yak.",
    "Z": " Zebra.",
    'Hello': "A good way to greet someone.",
    'Thanks': "Use this to show gratitude.",
    'Yes': "An affirmative gesture.",
    'No': "A negative gesture."
}

# Create a tkinter window
root = tk.Tk()
root.title("VAYUDASHA")
root.geometry("1200x600")  # Adjusted size to better fit components
# Function to introduce the application with a welcome message
def welcome_message():
    # Set the speech rate (lower values for slower speech)
    engine.setProperty('rate', 150)  # Adjust this value for desired speed (default ~200)

    # Set the pitch (not all voices support this, but you can try adjusting it)
    engine.setProperty('pitch', 70)  # Lower values for deeper pitch, higher for higher pitch

    # Speak the welcome message
    engine.say("Welcome to VAAYUDASHA, a sign language recognition application. Please make a gesture to start.")
    engine.runAndWait()

# Call the welcome message function
welcome_message()

# Add a label for dedication
dedication_label = tk.Label(root, text="KINDNESS IS A LANGUAGE WHICH THE DEAF CAN HEAR AND DUMB CAN SPEAK", font=("Noirden Sans", 16, "normal"))
dedication_label.pack(pady=(10, 10))  # Add some padding for aesthetics

# Tkinter variables
sentence_var = tk.StringVar()
suggestions_var = tk.StringVar()
voice_gender_var = tk.StringVar(value='Male')  # Default to male voice

# Create frames for layout
frame_video = tk.Frame(root)
frame_video.pack(side=tk.LEFT, padx=20)

frame_text = tk.Frame(root)
frame_text.pack(side=tk.RIGHT, padx=20)

# Create Canvas for video display
canvas = tk.Canvas(frame_video, width=640, height=480)
canvas.pack()

# Load the additional GIF using PIL and extract frames
gif_image = Image.open('./img1234.gif')  # Ensure the GIF is in the same directory
gif_frames = [ImageTk.PhotoImage(frame.resize((200, 200))) for frame in ImageSequence.Iterator(gif_image)]  # Resize to fit canvas

# Create a label for the text field
text_label = tk.Label(frame_text, text="Sentence:", font=("Helvetica", 14))
text_label.pack(pady=(0, 0))

# Create a Canvas for text field with a rectangle
text_canvas = tk.Canvas(frame_text, height=70, width=400, bg='white')
text_canvas.pack(pady=10)

# Draw a rectangle around the text field
text_canvas.create_rectangle(5, 5, 395, 65, outline="white", width=2)

# Create a text field in tkinter for the sentence (fully occupying the rectangle)
text_field = tk.Entry(text_canvas, textvariable=sentence_var, bg='white', font=("Helvetica", 16))
text_field.place(x=10, y=10, width=380, height=50)  # Fully occupy the rectangle box

# Create a label to display suggestions
suggestions_label = tk.Label(frame_text, textvariable=suggestions_var, font=("Helvetica", 12), wraplength=300)
suggestions_label.pack(pady=10)

# Function to update the tkinter sentence label and show suggestions based on the full sentence
def update_sentence(text):
    current_sentence = sentence_var.get()
    if text == 'space':
        new_sentence = current_sentence + ' '
    else:
        new_sentence = current_sentence + text
    sentence_var.set(new_sentence)
    logging.info(f'Word added: {text if text != "space" else "space (represented as space)"}')

    # Update suggestions based on the full sentence
    show_suggestion(new_sentence)

# Function to speak out the prediction using text-to-speech
def speak_prediction(prediction):
    engine.setProperty('rate', 150)  # Adjust this value for desired speed (default ~200)

    # Set the pitch (not all voices support this, but you can try adjusting it)
    engine.setProperty('pitch', 70)  # Lower values for deeper pitch, higher for higher pitch
    engine.say(prediction)
    engine.runAndWait()

# Function to show gesture suggestions based on the entire sentence
def show_suggestion(sentence):
    suggestion_text = ""
    for word in sentence.split():
        suggestion_text += suggestions_dict.get(word, "") + " | "
    suggestions_var.set(f"Gesture Suggestions: {suggestion_text.strip('| ')}")

# Function to clear the sentence
def clear_sentence():
    sentence_var.set('')  # Clear the sentence label
    suggestions_var.set('')  # Clear suggestions
    logging.info('Text cleared.')

# Function to speak the sentence
def speak_sentence():
    text = sentence_var.get().strip()
    if text:
        engine.say(text)
        engine.runAndWait()

# Create buttons for Clear, Speak, and Exit
clear_button = tk.Button(frame_text, text="Clear", command=clear_sentence)
clear_button.pack(pady=5)

speak_button = tk.Button(frame_text, text="Speak", command=speak_sentence)
speak_button.pack(pady=5)

exit_button = tk.Button(frame_text, text="Exit", command=root.quit)
exit_button.pack(pady=5)

# Create a dropdown menu for selecting voice gender
voice_gender_label = tk.Label(frame_text, text="Select Voice Gender:", font=("Helvetica", 12))
voice_gender_label.pack(pady=5)

voice_gender_menu = tk.OptionMenu(frame_text, voice_gender_var, 'Male', 'Female', command=set_voice_gender)
voice_gender_menu.pack(pady=5)

# Load the static image for the center display
center_image = Image.open('./title.png')  # Replace with your static image path
center_image = center_image.resize((300, 300))  # Resize to fit canvas
center_image_tk = ImageTk.PhotoImage(center_image)

# Create a canvas for the center image and display it
center_gif_canvas = tk.Canvas(root, width=300, height=300)
center_gif_canvas.pack(pady=10)  # Centered at the top
center_gif_canvas.create_image(0, 0, anchor=tk.NW, image=center_image_tk)
center_gif_canvas.image = center_image_tk  # Keep reference to avoid garbage collection

# Load additional GIF for gesture feedback and create canvas for GIF
gif_canvas = tk.Canvas(frame_text, width=200, height=200)
gif_canvas.pack(pady=10)

# Function to loop the additional GIF
def update_gif(frame_count=3):
    gif_canvas.delete("all")  # Clear the canvas
    gif_canvas.create_image(0, 0, anchor=tk.NW, image=gif_frames[frame_count])
    frame_count = (frame_count + 1) % len(gif_frames)  # Loop the GIF
    root.after(150, update_gif, frame_count)  # Adjust delay for slower frame rate (150ms)

# Function to run video capture and ISL prediction in a separate thread
def run():
    global last_detected_character, fixed_character, delayCounter, start_time

    last_detected_character = None
    delayCounter = 0
    start_time = time.time()

    while True:
        data_aux = []
        x_ = []
        y_ = []

        ret, frame = cap.read()

        if not ret:
            logging.error("Failed to capture video frame.")
            break

        frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirror effect
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                           mp_drawing_styles.get_default_hand_landmarks_style(),
                                           mp_drawing_styles.get_default_hand_connections_style())

                # Collect landmark positions
                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)

                # Calculate bounding box for the hand
                min_x, max_x = int(min(x_) * frame.shape[1]), int(max(x_) * frame.shape[1])
                min_y, max_y = int(min(y_) * frame.shape[0]), int(max(y_) * frame.shape[0])

                # Draw bounding box on the frame
                cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 3)

                # Prepare data for model prediction
                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

                # Predict the character
                prediction = model.predict([np.asarray(data_aux)])
                predicted_character = labels_dict[int(prediction[0])]

                # Place the label with the detected character above the bounding box
                cv2.putText(frame, predicted_character, (min_x, min_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

                # Add delay to prevent rapid updating
                if last_detected_character == predicted_character:
                    delayCounter += 1

                    if delayCounter == 5 and (time.time() - start_time) >= 0.25:
                        update_sentence(predicted_character)
                        speak_prediction(predicted_character)
                        delayCounter = 0
                        start_time = time.time()
                else:
                    delayCounter = 0

                last_detected_character = predicted_character

        # Update video display in the tkinter canvas
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
        canvas.image = imgtk

# Start the update_gif function in the main thread
update_gif()

# Run the video capture in a separate thread to keep tkinter responsive
threading.Thread(target=run, daemon=True).start()

# Start the tkinter main loop
root.mainloop()
