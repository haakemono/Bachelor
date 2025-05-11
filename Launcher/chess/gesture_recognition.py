# gesture_recognition.py
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

import sys
import os
import time

# 👇 Fix the module path BEFORE any imports from shared_input
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared_input.gesture import GestureRecognizer



# Mapping gestures to board file (column) and rank (row)
gesture_to_file = {
    'A': 0, 'B': 1, 'C': 2, 'D': 3,
    'E': 4, 'F': 5, 'G': 6, 'H': 7
}
gesture_to_rank = {
    'Y': 0, 'X': 1, 'O': 2, 'I': 3,
    'J': 4, 'K': 5, 'L': 6, 'P': 7
}

gesture_model = GestureRecognizer(
    valid_gestures=list(gesture_to_file.keys()) + list(gesture_to_rank.keys()),
    hold_time=2.0  # 2 seconds to confirm
)

def get_move_gesture():
    return gesture_model.get_latest_gesture()

def get_average_confidences():
    return gesture_model.get_average_confidences()

def print_average_confidences():
    gesture_model.print_average_confidences()

def release():
    gesture_model.release()

# Attach mappings for convenience in main.py
gesture_model.gesture_to_file = gesture_to_file
gesture_model.gesture_to_rank = gesture_to_rank
