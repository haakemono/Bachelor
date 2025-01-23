import cv2
import mediapipe as mp
from collections import deque

import time  # Import to track time


####HOVERING HAND TRACKER
class HandTracker:
    def __init__(self, width, smoothing_window_size=5, frame_skip=2):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.width = width
        self.smoothing_window_size = smoothing_window_size
        self.frame_skip = frame_skip
        self.frame_count = 0
        self.position_history = deque(maxlen=smoothing_window_size)
        self.hand_landmarks = None
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")

    def get_player_position(self):
        self.frame_count += 1

        if self.frame_count % self.frame_skip != 0:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        small_frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            self.hand_landmarks = results.multi_hand_landmarks[0]
            
            # Track the index finger tip (Landmark 8)
            index_finger_tip = self.hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_x = int((1 - index_finger_tip.x) * self.width)  # Invert x-axis for opposite movement
            player_y = int(index_finger_tip.y * self.width)  # Scale y-coordinate similarly
            
            # Append the new position to the history
            self.position_history.append((player_x, player_y))

        if self.position_history:
            # Smooth the position using the history
            smoothed_x, smoothed_y = map(
                lambda v: int(sum(v) / len(v)),
                zip(*self.position_history)
            )
            return smoothed_x, smoothed_y

        return None



    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.hands is not None:
            self.hands.close()
import cv2
import mediapipe as mp
from collections import deque

import time  # Import to track time


####HOVERING HAND TRACKER
class HandTracker:
    def __init__(self, width, smoothing_window_size=5, frame_skip=2):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.width = width
        self.smoothing_window_size = smoothing_window_size
        self.frame_skip = frame_skip
        self.frame_count = 0
        self.position_history = deque(maxlen=smoothing_window_size)
        self.hand_landmarks = None
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")

    def get_player_position(self):
        self.frame_count += 1

        if self.frame_count % self.frame_skip != 0:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        small_frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            self.hand_landmarks = results.multi_hand_landmarks[0]
            
            # Track the index finger tip (Landmark 8)
            index_finger_tip = self.hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_x = int((1 - index_finger_tip.x) * self.width)  # Invert x-axis for opposite movement
            player_y = int(index_finger_tip.y * self.width)  # Scale y-coordinate similarly
            
            # Append the new position to the history
            self.position_history.append((player_x, player_y))

        if self.position_history:
            # Smooth the position using the history
            smoothed_x, smoothed_y = map(
                lambda v: int(sum(v) / len(v)),
                zip(*self.position_history)
            )
            return smoothed_x, smoothed_y

        return None



    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.hands is not None:
            self.hands.close()
