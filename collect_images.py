import os
import cv2

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 44
dataset_size = 100

# Try using different camera indices if you have multiple cameras
cap = cv2.VideoCapture(0)  # Change 0 to the correct index for your camera
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

for j in range(number_of_classes):
    class_dir = os.path.join(DATA_DIR, str(j))
    if not os.path.exists(class_dir):
        os.makedirs(class_dir)

    print('Collecting data for class {}'.format(j))

    # Show frame until user presses 'q' to start collecting
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Display message on the frame
        cv2.putText(frame, 'Ready? Press "V" to start!', (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (235, 0, 135), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(25) & 0xFF == ord('v'):
            break

    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        cv2.imshow('frame', frame)
        cv2.waitKey(25)

        # Save the captured frame
        img_path = os.path.join(class_dir, '{}.jpg'.format(counter))
        cv2.imwrite(img_path, frame)

        counter += 1

    print(f"Data collection for class {j} completed.")

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()