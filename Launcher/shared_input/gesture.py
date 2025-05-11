from .base import load_model_and_scaler
import cv2
import numpy as np
import time
import mediapipe as mp
import threading

class GestureRecognizer:
    def __init__(self, valid_gestures=None, hold_time=0.5):
        self.model, self.label_encoder, self.scaler = load_model_and_scaler()
        self.hands = mp.solutions.hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(1)

        self.valid_gestures = valid_gestures
        self.hold_time = hold_time

        self.latest_gesture = None
        self.lock = threading.Lock()
        self.running = True

        self.thread = threading.Thread(target=self._gesture_loop)
        self.thread.daemon = True
        self.thread.start()



    """
    Continuously captures webcam frames and detects hand gestures in a background thread.

    - Uses MediaPipe to extract hand landmarks.
    - Scales the landmarks and feeds them into a trained gesture recognition model.
    - Checks if the predicted gesture matches the last one and is held for a specified duration.
    - If so, saves it as the latest confirmed gesture 
    - Runs until the tracker is released.
    """
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

                    if self.valid_gestures is None or gesture in self.valid_gestures:
                        if gesture == last_prediction:
                            if not gesture_start_time:
                                gesture_start_time = time.time()
                            elif time.time() - gesture_start_time >= self.hold_time:
                                with self.lock:
                                    self.latest_gesture = gesture
                                gesture_start_time = None
                        else:
                            last_prediction = gesture
                            gesture_start_time = None
            else:
                last_prediction = None
                gesture_start_time = None

            time.sleep(0.03)


    """
    Returns the most recently confirmed gesture and clears it.
    """
    def get_latest_gesture(self):
        with self.lock:
            g = self.latest_gesture
            self.latest_gesture = None
            return g


    """
    Stops the gesture recognition thread and releases all resources.
    - Releases the webcam and closes any OpenCV windows.
    """
    def release(self):
        self.running = False
        self.thread.join()
        self.cap.release()
        cv2.destroyAllWindows()
