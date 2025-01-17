import cv2
import mediapipe as mp
from collections import deque

class HandTracker:
    def __init__(self, width, smoothing_window_size=5, frame_skip=2):
        """
        Initializes the HandTracker.
        Args:
            width (int): The width of the screen where the basket position is mapped.
            smoothing_window_size (int): The number of recent positions to use for smoothing.
            frame_skip (int): The number of frames to skip for processing.
        """
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

    def get_basket_position(self):
        """
        Gets the basket position based on hand tracking.
        Returns:
            int: Smoothed basket position mapped to the screen width, or None if no position is detected.
        """
        self.frame_count += 1

        # Skip processing frames for optimization
        if self.frame_count % self.frame_skip != 0:
            return None

        ret, frame = self.cap.read()
        if not ret:
            print("Warning: Camera frame not read properly.")
            return None

        # Resize and process the frame for faster performance
        small_frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        # Get wrist position if at least one hand is detected
        if results.multi_hand_landmarks:
            self.hand_landmarks = results.multi_hand_landmarks[0]
            wrist = self.hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
            basket_x = int(wrist.x * self.width)
            self.position_history.append(basket_x)

        # Smooth the basket position
        if self.position_history:
            smoothed_x = int(sum(self.position_history) / len(self.position_history))
            return smoothed_x

        return None

    def release(self):
        """
        Releases the camera and closes the MediaPipe hands instance.
        """
        self.cap.release()
        self.hands.close()
