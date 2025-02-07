#constants.py

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
TOTAL_NOTES = 30 

# keybinds (temp)
KEYS = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]  
KEY_LABELS = ["A", "S", "D", "F"]

# hit zone
HIT_ZONE_X = 100  # where notes need to be hit
HIT_TOLERANCE = 20  # how close a note needs to be to count as a hit

# Font
pygame.font.init()
FONT = pygame.font.Font(None, 50)
