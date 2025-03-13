import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp
import pandas as pd

#  Load trained model and label encoder
model = tf.keras.models.load_model("gesture_recognition_model.h5")
label_encoder = joblib.load("label_encoder.pkl")

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

#  Start video capture
cap = cv2.VideoCapture(0)
last_prediction = None  # Store last recognized gesture to prevent redundant output

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for natural hand tracking
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark coordinates
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])  # Flatten x, y, z coordinates

            # Convert to a NumPy array and reshape for model prediction
            landmarks = np.array(landmarks, dtype=np.float32).reshape(1, -1)

            # 🔹 Ensure consistency with model input format
            if landmarks.shape[1] == model.input_shape[1]:  # Input dimension check
                prediction = model.predict(landmarks, verbose=0)  #  Suppress printing
                predicted_class = np.argmax(prediction)  # Get highest probability class
                gesture_name = label_encoder.inverse_transform([predicted_class])[0]

                #  Print only when the gesture changes
                if gesture_name != last_prediction:
                    print(f" Detected Gesture: {gesture_name}")
                    last_prediction = gesture_name  # Update last recognized gesture

                # Display result on screen
                cv2.putText(frame, f'Gesture: {gesture_name}', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow("Gesture Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
