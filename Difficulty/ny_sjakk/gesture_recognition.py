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

        # **🔹 CUSTOMIZABLE Gesture Mappings**
        # Change these to match the gestures you want to use
        self.gesture_to_file = {   # File (Column) Mapping
            "A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7
        }
        self.gesture_to_rank = {   # Rank (Row) Mapping
            "Y": 0, "X": 1, "O": 2, "I": 3, "J": 4, "K": 5, "L": 6, "P": 7
        }

        # **🔹 EXAMPLE ALTERNATIVE MAPPINGS**
        # If you want to use "Left" instead of "A" for column A:
        # self.gesture_to_file = { "Left": 0, "Right": 7 }  

        # If you want "Y" to represent rank 1 instead of "1":
        # self.gesture_to_rank = { "Y": 0, "X": 7 }  

    def get_gesture(self):
        """
        Captures a frame, processes hand landmarks, and predicts a gesture.
        Returns:
            str: Confirmed gesture if held for 2 seconds, otherwise None.
        """
        ret, frame = self.cap.read()
        if not ret:
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

                    # **🔹 Require Gesture to Be Held for 2 Seconds**
                    if gesture_name == self.last_prediction:
                        if self.gesture_start_time is None:
                            self.gesture_start_time = time.time()  # Start timer
                        elif time.time() - self.gesture_start_time >= 1:  # Check if 2 seconds passed
                            return gesture_name  # Confirmed gesture
                    else:
                        self.last_prediction = gesture_name
                        self.gesture_start_time = None  # Reset timer

        return None

    def release(self):
        """Releases the camera resources."""
        self.cap.release()
        cv2.destroyAllWindows()
