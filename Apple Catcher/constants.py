# constants.py
import pygame

# Game dimensions
WIDTH = 1000
HEIGHT = 800

# Player settings
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20
PLAYER_VEL = 10

# Apple settings
APPLE_RADIUS = 15
APPLE_FALL_SPEED = 10
NEW_APPLE_INTERVAL = 150

# Bomb settings
BOMB_RADIUS = 15
BOMB_FALL_SPEED = 8
NEW_BOMB_INTERVAL = 240

# Font
pygame.font.init()
FONT = pygame.font.Font(None, 36)
