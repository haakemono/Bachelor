import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from shared_input.gesture import GestureRecognizer

gesture_model = GestureRecognizer(valid_gestures=['A', 'S', 'D', 'F'])

gesture_to_key = {
    'A': pygame.K_a,
    'S': pygame.K_s,
    'D': pygame.K_d,
    'F': pygame.K_f
}

def get_gesture_keypress():
    gesture = gesture_model.get_latest_gesture()
    if gesture and gesture in gesture_to_key:
        return gesture_to_key[gesture]
    return None

def release_gesture_resources():
    gesture_model.release()
