import os
import pickle
import re
import mediapipe as mp
import cv2


# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Set up the hands detection with MediaPipe
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'

data = []
labels = []

# Function to sort filenames naturally (e.g., 0, 1, 2, ..., 10, 11, ...)
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# Iterate over directories in the DATA_DIR in sorted order
for dir_ in sorted(os.listdir(DATA_DIR), key=natural_sort_key):
    dir_path = os.path.join(DATA_DIR, dir_)

    # Check if dir_path is a directory to avoid NotADirectoryError
    if os.path.isdir(dir_path):
        print(f"Processing directory: {dir_path}")

        # Iterate over images in the directory in sorted order using natural sorting
        for img_path in sorted(os.listdir(dir_path), key=natural_sort_key):
            img_full_path = os.path.join(dir_path, img_path)

            # Ensure the file is an image file
            if os.path.isfile(img_full_path) and img_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Processing file: {img_full_path}")

                data_aux = []
                x_ = []
                y_ = []
                z_ = []  # Added for z-coordinate

                # Read image using OpenCV
                img = cv2.imread(img_full_path)
                if img is None:
                    print(f"Error: Unable to read the image file {img_full_path}")
                    continue

                # Convert the BGR image to RGB for MediaPipe processing
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                # Process the image and find hand landmarks
                results = hands.process(img_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Collect landmark coordinates (x, y, and z)
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            z = hand_landmarks.landmark[i].z  # Collect z-coordinate
                            x_.append(x)
                            y_.append(y)
                            z_.append(z)  # Add z-coordinates to the list

                        # Normalize landmarks relative to the minimum x, y, and z coordinates
                        for i in range(len(hand_landmarks.landmark)):
                            x = hand_landmarks.landmark[i].x
                            y = hand_landmarks.landmark[i].y
                            z = hand_landmarks.landmark[i].z
                            data_aux.append(x - min(x_))
                            data_aux.append(y - min(y_))
                            data_aux.append(z - min(z_))  # Include normalized z-coordinates

                    # Append the processed data and label to lists
                    data.append(data_aux)
                    labels.append(dir_)
                else:
                    print(f"No hand landmarks detected in {img_full_path}. Skipping this image.")
            else:
                print(f"Skipping non-image file: {img_full_path}")
    else:
        print(f"Skipping non-directory item: {dir_path}")

# Check if we have 84 features (21 landmarks * 3 coordinates = 63 for one hand; double for two hands)
# If only one hand is present, pad with zeros to make up the difference
final_data = []
for item in data:
    if len(item) < 84:
        # Padding with zeros if fewer than 84 features
        item += [0] * (84 - len(item))
    final_data.append(item)

# Save the data and labels to a pickle file
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': final_data, 'labels': labels}, f)

print("Data processing complete. Data saved to 'data.pickle'.")



