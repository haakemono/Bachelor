#constants.py

import os
import pygame

# dimensions
WIDTH, HEIGHT = 1200, 800

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)

# notes
NOTE_SPEED = 6
TOTAL_NOTES = 32 

# keybinds (temp)
KEYS = {'A': pygame.K_a, 'S': pygame.K_s, 'D': pygame.K_d, 'F': pygame.K_f}
KEY_LABELS = ["A", "S", "D", "F"]

# hit zone
HIT_ZONE_X = 100  # where notes need to be hit
HIT_TOLERANCE = 20  # how close a note needs to be to count as a hit

# font
pygame.font.init()
FONT = pygame.font.Font(None, 50)

#music file
MUSIC_FILE = os.path.join(os.path.dirname(__file__), "music", "Level 1.mp3")

