import os
import pygame

# dimensions
WIDTH, HEIGHT = 1200, 800

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GRAY = (100, 100, 100)
PURPLE = (128, 0, 128)

#notes (WARNING: changing these can break existing songs)
NOTE_SPEED = 6
TOTAL_NOTES = 32 

#keybinds (remember to make corresponding changes in the beatmaps as well)
KEYS = {'A': pygame.K_a, 'S': pygame.K_s, 'D': pygame.K_d, 'F': pygame.K_f}
KEY_LABELS = ["A", "S", "D", "F"]

# hit zone
HIT_ZONE_X = 300  # where notes need to be hit
HIT_TOLERANCE = 100  # how close a note needs to be to count as a hit, counts both before and after a note has passed
# font
pygame.font.init()
FONT = pygame.font.Font(None, 50)

