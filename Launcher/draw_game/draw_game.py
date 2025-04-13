import pygame
import sys
import time
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

COLOR_OPTIONS = [RED, GREEN, BLUE, BLACK]
CLEAR_OPTION_Y = HEIGHT - 80

# Setup screen & canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Drawing App")
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

font = pygame.font.SysFont(None, 24)

selected_color = BLACK
drawing = False
last_tool_change = 0
TOOL_CHANGE_COOLDOWN = 1.5  # seconds

clock = pygame.time.Clock()

def draw_toolbar():
    pygame.draw.rect(screen, (200, 200, 200), (0, 0, TOOLBAR_WIDTH, HEIGHT))
    for i, color in enumerate(COLOR_OPTIONS):
        pygame.draw.rect(screen, color, (20, 20 + i * 60, 60, 40))
        if selected_color == color:
            pygame.draw.rect(screen, BLACK, (20, 20 + i * 60, 60, 40), 3)
    pygame.draw.rect(screen, (180, 180, 180), (20, CLEAR_OPTION_Y, 60, 40))
    text = font.render("CLEAR", True, BLACK)
    screen.blit(text, (25, CLEAR_OPTION_Y + 10))

def in_toolbar(px, py):
    return px < TOOLBAR_WIDTH

# Main loop
last_pos = None

running = True
while running:
    finger_pos = get_finger_position()
    gesture = get_gesture_command()
    current_time = time.time()

    # === Handle gestures ===
    if gesture:
        print(f"[Gesture Detected] {gesture}")
        if gesture == "F":
            drawing = True
            print("Drawing mode ON")
        elif gesture == "STOP":
            drawing = False
            print("Drawing mode OFF")
        elif current_time - last_tool_change > TOOL_CHANGE_COOLDOWN:
            if gesture == "A":
                selected_color = RED
                last_tool_change = current_time
                print("Switched to RED")
            elif gesture == "B":
                selected_color = BLUE
                last_tool_change = current_time
                print("Switched to BLUE")
            elif gesture == "C":
                selected_color = GREEN
                last_tool_change = current_time
                print("Switched to GREEN")
            elif gesture == "D":
                canvas.fill(WHITE)
                last_tool_change = current_time
                print("Canvas cleared")
            elif gesture == "E":
                selected_color = WHITE
                last_tool_change = current_time
                print("Eraser selected")

    # === Drawing logic ===
    if finger_pos:
        x, y = finger_pos
        print(f"Finger Position: {x}, {y} | Drawing: {drawing}")

        if drawing and not in_toolbar(x, y):
            if last_pos:
                pygame.draw.line(canvas, selected_color, last_pos, (x, y), PEN_RADIUS * 2)
                print(f"Line drawn from {last_pos} to {(x, y)}")
            else:
                pygame.draw.circle(canvas, selected_color, (x, y), PEN_RADIUS)
                print(f"Dot drawn at {(x, y)}")
            last_pos = (x, y)
        else:
            last_pos = None  # stop connecting lines when not drawing

    # === Handle events ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # === Render everything ===
    screen.blit(canvas, (0, 0))
    draw_toolbar()
    if finger_pos:
        pygame.draw.circle(screen, BLACK, finger_pos, POINTER_RADIUS, 1)
    pygame.display.flip()
    clock.tick(60)