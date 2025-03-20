# --- gesture_recognition.py ---

import os
import time
import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp
import warnings

# Suppress sklearn warnings
warnings.simplefilter(action='ignore', category=UserWarning)

class GestureRecognizer:
    def __init__(self, model_path="gesture_recognition_model.h5", encoder_path="label_encoder.pkl", scaler_path="scaler.pkl"):
        base_path = os.path.dirname(__file__)
        self.model = tf.keras.models.load_model(os.path.join(base_path, model_path))
        self.label_encoder = joblib.load(os.path.join(base_path, encoder_path))
        self.scaler = joblib.load(os.path.join(base_path, scaler_path))

        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        # Camera setup
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Default camera not found. Trying alternative index (1)...")
            self.cap = cv2.VideoCapture(1)

        # Gesture hold tracking
        self.last_prediction = None
        self.gesture_start_time = None

        # Gesture mappings
        self.gesture_to_file = {k: i for i, k in enumerate("ABCDEFGH")}
        self.gesture_to_rank = {k: i for i, k in enumerate("YXOIJKLP")}  # Adjust if needed

        # Confidence tracking
        self.gesture_confidences = {label: {"total_confidence": 0.0, "count": 0} for label in self.label_encoder.classes_}

    def get_move_gesture(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Camera capture failed.")
            return None

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten().reshape(1, -1)

                if landmarks.shape[1] != self.model.input_shape[1]:
                    continue

                scaled = self.scaler.transform(landmarks)
                prediction = self.model.predict(scaled, verbose=0)[0]
                gesture_index = np.argmax(prediction)
                gesture = self.label_encoder.inverse_transform([gesture_index])[0]
                confidence = prediction[gesture_index] * 100

                print(f"Gesture: {gesture}, Confidence: {confidence:.1f}%")

                self.gesture_confidences[gesture]["total_confidence"] += confidence
                self.gesture_confidences[gesture]["count"] += 1

                if gesture in self.gesture_to_file or gesture in self.gesture_to_rank:
                    if gesture == self.last_prediction:
                        if not self.gesture_start_time:
                            self.gesture_start_time = time.time()
                        elif time.time() - self.gesture_start_time >= 2:
                            self.gesture_start_time = None
                            return gesture
                    else:
                        self.last_prediction = gesture
                        self.gesture_start_time = None
        return None

    def print_average_confidences(self):
        print("\n--- Average Gesture Confidence ---")
        for gesture, stats in self.gesture_confidences.items():
            count = stats["count"]
            if count > 0:
                avg_conf = stats["total_confidence"] / count
                print(f"{gesture}: {avg_conf:.1f}% average confidence over {count} detections")
            else:
                print(f"{gesture}: No detections")

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

