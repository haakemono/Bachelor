import pygame
import sys

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
SPEED = 5

# Colors and options
COLOR_OPTIONS = [RED, GREEN, BLUE, BLACK]
CLEAR_OPTION_Y = HEIGHT - 80  # Position of "CLEAR" button

# Setup screen & canvas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toolbar Drawing App")
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

# Setup font
font = pygame.font.SysFont(None, 24)

# Initial position and color
x, y = WIDTH // 2, HEIGHT // 2
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
    keys = pygame.key.get_pressed()

    dx = dy = 0
    if keys[pygame.K_LEFT]:
        dx = -SPEED
    if keys[pygame.K_RIGHT]:
        dx = SPEED
    if keys[pygame.K_UP]:
        dy = -SPEED
    if keys[pygame.K_DOWN]:
        dy = SPEED

    x += dx
    y += dy
    x = max(0, min(WIDTH, x))
    y = max(0, min(HEIGHT, y))

    if keys[pygame.K_SPACE]:
        selection = get_toolbar_selection(x, y)
        if selection == "CLEAR":
            canvas.fill(WHITE)
        elif selection in COLOR_OPTIONS:
            selected_color = selection
        elif not in_toolbar(x, y):
            pygame.draw.circle(canvas, selected_color, (x, y), PEN_RADIUS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.blit(canvas, (0, 0))
    draw_toolbar()
    pygame.draw.circle(screen, BLACK, (x, y), POINTER_RADIUS, 1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
