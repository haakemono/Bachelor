# gesture_input.py – med trådbasert gesture-scanning

import os
import time
import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp
import pygame
import threading
import warnings

warnings.simplefilter(action='ignore', category=UserWarning)

class GestureRecognizer:
    def __init__(self, model_path="gesture_recognition_model.h5", encoder_path="label_encoder.pkl", scaler_path="scaler.pkl"):
        base_path = os.path.dirname(__file__)
        self.model = tf.keras.models.load_model(os.path.join(base_path, model_path))
        self.label_encoder = joblib.load(os.path.join(base_path, encoder_path))
        self.scaler = joblib.load(os.path.join(base_path, scaler_path))

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Default camera not found. Trying alternative index (1)...")
            self.cap = cv2.VideoCapture(1)

        # Gyldige gester og mapping
        self.gesture_to_key = {
            'A': pygame.K_a,
            'S': pygame.K_s,
            'D': pygame.K_d,
            'F': pygame.K_f
        }
        self.valid_gestures = list(self.gesture_to_key.keys())

        # Resultat
        self.latest_key = None
        self.lock = threading.Lock()
        self.running = True

        # Start bakgrunnstråd
        self.thread = threading.Thread(target=self._gesture_loop)
        self.thread.daemon = True
        self.thread.start()

    def _gesture_loop(self):
        last_prediction = None
        gesture_start_time = None

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

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

                    if gesture in self.valid_gestures:
                        if gesture == last_prediction:
                            if not gesture_start_time:
                                gesture_start_time = time.time()
                            elif time.time() - gesture_start_time >= 0.5:
                                with self.lock:
                                    self.latest_key = self.gesture_to_key[gesture]
                                print(f"✅ Gesture recognized: {gesture} ({confidence:.1f}%)")
                                gesture_start_time = None
                        else:
                            last_prediction = gesture
                            gesture_start_time = None
            else:
                last_prediction = None
                gesture_start_time = None

            time.sleep(0.03)  # ~30 fps

    def get_latest_key(self):
        with self.lock:
            key = self.latest_key
            self.latest_key = None
            return key

    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()
        cv2.destroyAllWindows()

# Global instans
gesture_model = GestureRecognizer()

def get_gesture_keypress():
    return gesture_model.get_latest_key()

def release_gesture_resources():
    gesture_model.release()
