import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp
import time
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)  # Suppress sklearn warning

class GestureRecognizer:
    def __init__(self, model_path="gesture_recognition_model.h5", encoder_path="label_encoder.pkl", scaler_path="scaler.pkl"):
        # Load trained model, label encoder, and scaler
        self.model = tf.keras.models.load_model(model_path)
        self.label_encoder = joblib.load(encoder_path)
        self.scaler = joblib.load(scaler_path)

        # Initialize MediaPipe Hand Tracking
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        # Start video capture
        self.cap = cv2.VideoCapture(0)
        self.last_prediction = None
        self.gesture_start_time = None

        # **Mapping for move gestures (file and rank)**
        self.gesture_to_file = {   # File (Column) Mapping
            "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7
        }
        self.gesture_to_rank = {   # Rank (Row) Mapping
            "Y": 0, "X": 1, "O": 2, "I": 3, "J": 4, "K": 5, "L": 6, "P": 7
        }

    def get_move_gesture(self):
        """
        Captures a gesture for selecting a chess piece's file (column) or rank (row).
        Returns:
            str: The selected gesture (file or rank).
        """
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame")
            return None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

                landmarks = np.array(landmarks, dtype=np.float32).reshape(1, -1)

                if landmarks.shape[1] == self.model.input_shape[1]:
                    landmarks_scaled = self.scaler.transform(landmarks)
                    prediction = self.model.predict(landmarks_scaled, verbose=0)
                    predicted_class = np.argmax(prediction)
                    gesture_name = self.label_encoder.inverse_transform([predicted_class])[0]

                    # Only accept valid gestures from the defined mappings
                    if gesture_name in self.gesture_to_file or gesture_name in self.gesture_to_rank:
                        print(f"Captured gesture: {gesture_name}")  # Debug print

                        # **🔹 Require Gesture to Be Held for 2 Seconds**
                        if gesture_name == self.last_prediction:
                            if self.gesture_start_time is None:
                                self.gesture_start_time = time.time()  # Start timer
                            elif time.time() - self.gesture_start_time >= 2:  # Check if 2 seconds passed
                                self.last_prediction = gesture_name
                                self.gesture_start_time = None  # Reset timer after valid gesture
                                return gesture_name  # Return valid gesture
                        else:
                            self.last_prediction = gesture_name
                            self.gesture_start_time = None  # Reset timer if gesture changes

        return None

    def release(self):
        """Releases the camera resources."""
        self.cap.release()
        cv2.destroyAllWindows()