import cv2
import mediapipe as mp
from collections import deque
import threading
import numpy as np

# -------------------------------
# HAND TRACKING CONTROLLER 
# -------------------------------

class HandTracker:
    def __init__(self, width, smoothing_window_size=5):
        self.width = width
        self.smoothing_window_size = smoothing_window_size
        self.position_history = deque(maxlen=smoothing_window_size)
        self.hand_landmarks = None
        self.running = True
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5, max_num_hands=1)

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")
        
        self.frame = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.thread.start()



    """
    Continuously captures frames from the webcam in a background thread.

    - Resizes each frame to 320x240.
    - Stores the latest frame in a shared variable with thread-safe access.
    """
    def _capture_frames(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = cv2.resize(frame, (320, 240))


    """
    Processes the latest captured frame to estimate the player's horizontal position.

    - Converts the frame to RGB and runs hand landmark detection.
    - Extracts the x-position of the index fingertip.
    - Scales the x-position to the game width and stores it in a position history buffer.
    """
    def get_player_position(self):
        with self.lock:
            if self.frame is None:
                return None
            frame = self.frame.copy()

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            index_finger_tip = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_x = int(index_finger_tip.x * self.width)
            self.position_history.append(player_x)

        if self.position_history:
            return self._exponential_smoothing()

        return None


    """
    Applies smoothing to the player's recent x-positions.

    - Uses the position history to reduce jitter in hand movement.
    - The smoothing factor 'alpha' controls responsiveness (closer to 1 = more responsive).
    - Returns the final smoothed x-position as an integer.
    """
    def _exponential_smoothing(self, alpha=0.3):
        smoothed_x = self.position_history[0]
        for x in self.position_history:
            smoothed_x = alpha * x + (1 - alpha) * smoothed_x
        return int(smoothed_x)


    """
    Shuts down the hand tracker and releases all resources.
    """
    def release(self):
        self.running = False
        self.thread.join()
        if self.cap.isOpened():
            self.cap.release()
        if self.hands is not None:
            self.hands.close()
        self.frame = None
        self.position_history.clear()

# -------------------------------
# BALL TRACKING CONTROLLER
# -------------------------------

class BallTracker:
    def __init__(self, width):
        self.width = width
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")

        self.tracker = None
        self.tracking = False
        self.bbox = None

        # Hardcoded best tracking parameters
        self.min_radius = 20
        self.max_radius = 90
        self.param1 = 50
        self.param2 = 65
        self.min_dist = 39


    """
    Detects a ball in the given frame using the Hough Circle Transform.

    - Converts the frame to grayscale and applies Gaussian blur.
    - Uses predefined parameters to detect circles (potential balls).
    - Returns a bounding box (x, y, width, height) around the first detected circle.
    """
    def detect_ball(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=self.min_dist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )

        if circles is not None:
            circles = np.uint16(np.around(circles[0, :]))
            x, y, r = circles[0]
            x, y, r = int(x), int(y), int(r)
            bbox = (x - r, y - r, r * 2, r * 2)
            return bbox
        return None


    """
    Initializes the KCF tracker with the given frame and bounding box.

    - Starts tracking the specified bounding box within the frame.
    """
    def initialize_tracker(self, frame, bbox):
        self.tracker = cv2.TrackerKCF_create()  
        self.tracker.init(frame, bbox)
        self.tracking = True
        self.bbox = bbox


    """
    Updates the tracker with a new frame to follow the ball's movement.
    """
    def update_tracker(self, frame):
        success, bbox = self.tracker.update(frame)
        if success:
            self.bbox = bbox
            return True
        else:
            self.tracking = False
            self.tracker = None
            return False


    """
    Determines the player's horizontal position based on the tracked ball.

    - Captures a new frame and horizontally flips it.
    - If tracking is active, attempts to update the tracker.
        - If tracking fails, re-detects the ball and reinitializes tracking.
    - If tracking is successful, calculates the horizontal center of the ball
      and scales it to the game width.
    """
    def get_player_position(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)

        if self.tracking:
            success = self.update_tracker(frame)
            if not success:
                bbox = self.detect_ball(frame)
                if bbox:
                    self.initialize_tracker(frame, bbox)
        else:
            bbox = self.detect_ball(frame)
            if bbox:
                self.initialize_tracker(frame, bbox)

        if self.tracking:
            x, y, w, h = [int(v) for v in self.bbox]
            center_x = x + w // 2
            return int(center_x * self.width / frame.shape[1])  # Scale to game width

        return None

    """
    Releases the webcam resource if it is currently open.
    """
    def release(self):
        if self.cap.isOpened():
            self.cap.release()
