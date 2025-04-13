import os
import cv2
import numpy as np
import tensorflow as tf
import joblib
import mediapipe as mp
import threading
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class HandTracker:
    def __init__(self, model_path="gesture_recognition_model.h5", encoder_path="label_encoder.pkl", scaler_path="scaler.pkl"):
        base_path = os.path.dirname(__file__)
        self.model = tf.keras.models.load_model(os.path.join(base_path, model_path))
        self.label_encoder = joblib.load(os.path.join(base_path, encoder_path))
        self.scaler = joblib.load(os.path.join(base_path, scaler_path))

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)

        self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.latest_position = None
        self.latest_gesture = None
        self.lock = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self._loop)
        self.thread.daemon = True
        self.thread.start()

    def _loop(self):
        last_gesture = None
        gesture_start = None

        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            with self.lock:
                self.latest_position = None
                self.latest_gesture = None

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    flat_landmarks = landmarks.flatten().reshape(1, -1)

                    if flat_landmarks.shape[1] != self.model.input_shape[1]:
                        continue

                    scaled = self.scaler.transform(flat_landmarks)
                    prediction = self.model.predict(scaled, verbose=0)[0]
                    gesture_index = np.argmax(prediction)
                    gesture = self.label_encoder.inverse_transform([gesture_index])[0]
                    confidence = prediction[gesture_index] * 100

                    # Check for gesture hold (1s)
                    if gesture == last_gesture:
                        if gesture_start and (cv2.getTickCount() - gesture_start) / cv2.getTickFrequency() > 1:
                            with self.lock:
                                self.latest_gesture = gesture
                            gesture_start = None
                    else:
                        last_gesture = gesture
                        gesture_start = cv2.getTickCount()

                    # Save finger position (index tip)
                    index_finger = landmarks[8]
                    screen_x = int(index_finger[0] * 800)  # scale to Pygame 800x600
                    screen_y = int(index_finger[1] * 600)
                    with self.lock:
                        self.latest_position = (screen_x, screen_y)
                    break

            cv2.waitKey(1)

    def get_finger_position(self):
        with self.lock:
            return self.latest_position

    def get_gesture_command(self):
        with self.lock:
            gesture = self.latest_gesture
            self.latest_gesture = None
            return gesture

    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()
        cv2.destroyAllWindows()

# Singleton-like access
tracker = HandTracker()

def get_finger_position():
    return tracker.get_finger_position()

def get_gesture_command():
    return tracker.get_gesture_command()

def release_hand_tracker():
    tracker.release()
