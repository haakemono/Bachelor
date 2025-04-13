
import pygame
import sys
from hand_tracking import get_finger_position, get_gesture_command, release_hand_tracker

# Initialize
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
TOOLBAR_WIDTH = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE  = (0, 100, 255)

PEN_RADIUS = 4
POINTER_RADIUS = 6

# Colors and options
COLOR_OPTIONS = [RED, GREEN, BLUE, BLACK]
CLEAR_OPTION_Y = HEIGHT - 80  # Position of "CLEAR" button

# Setup screen & canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Drawing App")
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Setup font
font = pygame.font.SysFont(None, 24)

# Initial color
selected_color = BLACK
clock = pygame.time.Clock()

def draw_toolbar():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, TOOLBAR_WIDTH, HEIGHT))

    # Draw color buttons
    for i, color in enumerate(COLOR_OPTIONS):
        pygame.draw.rect(screen, color, (20, 20 + i * 60, 60, 40))
        if selected_color == color:
            pygame.draw.rect(screen, BLACK, (20, 20 + i * 60, 60, 40), 3)

    # Draw clear button
    pygame.draw.rect(screen, (180, 180, 180), (20, CLEAR_OPTION_Y, 60, 40))
    text = font.render("CLEAR", True, BLACK)
    screen.blit(text, (25, CLEAR_OPTION_Y + 10))

def in_toolbar(px, py):
    return px < TOOLBAR_WIDTH

def get_toolbar_selection(px, py):
    if px > TOOLBAR_WIDTH:
        return None
    for i, color in enumerate(COLOR_OPTIONS):
        rect = pygame.Rect(20, 20 + i * 60, 60, 40)
        if rect.collidepoint(px, py):
            return color
    clear_rect = pygame.Rect(20, CLEAR_OPTION_Y, 60, 40)
    if clear_rect.collidepoint(px, py):
        return "CLEAR"
    return None

running = True
while running:
    drawing = False

    finger_pos = get_finger_position()
    gesture = get_gesture_command()

    if finger_pos:
        x, y = finger_pos

        # Tegn kun hvis utenfor toolbar og gesturen tilsier "tegn"
        # Oppdater "drawing" status basert på gesture
        if gesture == "F":
            drawing = True
        elif gesture is not None:
            drawing = False

        # Tegn så lenge "drawing" er aktiv
        if drawing and not in_toolbar(x, y):
            pygame.draw.circle(canvas, selected_color, (x, y), PEN_RADIUS)


        # Gestures som handlinger
        if gesture == "A":
            selected_color = RED
        elif gesture == "B":
            selected_color = BLUE
        elif gesture == "C":
            selected_color = GREEN
        elif gesture == "D":
            canvas.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(canvas, (0, 0))
    draw_toolbar()
    if finger_pos:
        pygame.draw.circle(screen, BLACK, (x, y), POINTER_RADIUS, 1)

    pygame.display.flip()
    clock.tick(60)

release_hand_tracker()
pygame.quit()
sys.exit()
