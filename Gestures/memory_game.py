import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import joblib
import random
import time
import os

# Suppress TensorFlow logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load trained model and label encoder
model = tf.keras.models.load_model("gesture_model.keras")
label_encoder = joblib.load("label_encoder.pkl")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# List of gestures that can be used in the game
GESTURES = ["Thumbs Up", "Peace Sign", "Fist", "OK Sign", "Rock Sign", "Stop Sign", "Thumbs Down", "Love"]

# Game variables
sequence = []  # Stores the correct sequence
user_sequence = []  # Stores what the user does
current_index = 0  # Index to track progress in the sequence
lock_duration = 2  # Time in seconds the user must hold a gesture
last_gesture = None
gesture_start_time = None
game_over = False

def add_new_gesture():
    """Adds a new random gesture to the sequence."""
    new_gesture = random.choice(GESTURES)
    sequence.append(new_gesture)

def display_sequence():
    """Displays the sequence one by one."""
    print("\n🧠 Memorize this sequence:")
    for i, gesture in enumerate(sequence):
        print(f"🔹 {i + 1}. {gesture}")
        time.sleep(1)  # Pause for readability

def detect_gesture(frame):
    """Detects the user's hand gesture using the model."""
    global last_gesture, gesture_start_time
    detected_gesture = None

    # Convert frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark features (21 points with x, y, z)
            landmark_data = []
            for landmark in hand_landmarks.landmark:
                landmark_data.extend([landmark.x, landmark.y, landmark.z])

            # Convert to NumPy array and predict gesture
            landmark_array = np.array(landmark_data).reshape(1, -1)
            prediction = model.predict(landmark_array, verbose=0)
            predicted_label = label_encoder.inverse_transform([np.argmax(prediction)])[0]

            if predicted_label in GESTURES:
                detected_gesture = predicted_label

    # Check if the user holds the same gesture for enough time
    if detected_gesture:
        if detected_gesture == last_gesture:
            if time.time() - gesture_start_time >= lock_duration:
                return detected_gesture  # Gesture confirmed
        else:
            last_gesture = detected_gesture
            gesture_start_time = time.time()

    return None

# Start the game
print("\n🎮 Welcome to the Gesture Memory Game! Try to follow the growing sequence of gestures.")

# First gesture
add_new_gesture()

while not game_over:
    display_sequence()
    user_sequence = []
    current_index = 0

    print("\n🤚 Now it's your turn! Repeat the sequence correctly.")

    while current_index < len(sequence):
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame.")
            break

        # Detect gesture from the frame
        detected_gesture = detect_gesture(frame)

        # Show live camera feed
        cv2.putText(frame, "Follow the Sequence!", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if detected_gesture:
            cv2.putText(frame, f"Detected: {detected_gesture}", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Gesture Memory Game", frame)

        if detected_gesture:
            print(f"✔️ Detected: {detected_gesture}")
            user_sequence.append(detected_gesture)

            # Check if the user's input matches the sequence
            if user_sequence[current_index] != sequence[current_index]:
                game_over = True
                break

            current_index += 1
            time.sleep(1)  # Pause between gestures

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            game_over = True
            break

    if not game_over:
        print("\n🎉 Correct! The sequence grows longer...\n")
        add_new_gesture()
        time.sleep(2)

# Game over message
print("\n❌ Game Over!")
print(f"🏆 Your final score: {len(sequence) - 1} rounds.")

cap.release()
cv2.destroyAllWindows()
