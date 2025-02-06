import cv2
import mediapipe as mp
from collections import deque
import threading

class HandTracker:
    def __init__(self, width, smoothing_window_size=5):
        self.width = width
        self.smoothing_window_size = smoothing_window_size
        self.position_history = deque(maxlen=smoothing_window_size)
        self.hand_landmarks = None
        self.running = True  # Thread control flag
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")
        
        # Start a thread for continuous frame reading
        self.frame = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()

    def _capture_frames(self):
        """Continuously capture frames in a separate thread."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = cv2.resize(frame, (320, 240))  # Lower resolution for speed

    def get_player_position(self):
        """Get the x-position of the index finger tip."""
        with self.lock:
            if self.frame is None:
                return None
            frame = self.frame.copy()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            # Track the index finger tip (landmark 8)
            index_finger_tip = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_x = int(index_finger_tip.x * self.width)
            self.position_history.append(player_x)

        if self.position_history:
            return self._exponential_smoothing()

        return None

    def _exponential_smoothing(self, alpha=0.3):
        """Apply exponential smoothing to the position history."""
        smoothed_x = self.position_history[0]
        for x in self.position_history:
            smoothed_x = alpha * x + (1 - alpha) * smoothed_x
        return int(smoothed_x)

    def release(self):
        """Release resources properly and stop frame capture thread."""
        self.running = False
        self.thread.join()
        if self.cap.isOpened():
            self.cap.release()
        if self.hands is not None:
            self.hands.close()
        self.frame = None
        self.position_history.clear()
    