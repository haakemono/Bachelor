import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Catcher")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)  # Color for bombs

# Basket variables
basket_width, basket_height = 100, 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 20
basket_speed = 10

# Apple variables
apple_radius = 15
apple_x = random.randint(apple_radius, WIDTH - apple_radius)
apple_y = -apple_radius
apple_speed = 5

# Bomb variables
bomb_radius = 15
bomb_x = random.randint(bomb_radius, WIDTH - bomb_radius)
bomb_y = -bomb_radius
bomb_speed = 4

# Game variables
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)

# Clock to control frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Basket movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Update apple position
    apple_y += apple_speed

    # Check if apple is caught
    if basket_y <= apple_y + apple_radius <= basket_y + basket_height and basket_x <= apple_x <= basket_x + basket_width:
        score += 1
        apple_x = random.randint(apple_radius, WIDTH - apple_radius)
        apple_y = -apple_radius

    # Check if apple hits the ground
    if apple_y > HEIGHT:
        lives -= 1
        apple_x = random.randint(apple_radius, WIDTH - apple_radius)
        apple_y = -apple_radius

    # Update bomb position
    bomb_y += bomb_speed

    # Check if bomb hits the basket
    if basket_y <= bomb_y + bomb_radius <= basket_y + basket_height and basket_x <= bomb_x <= basket_x + basket_width:
        lives -= 1
        bomb_x = random.randint(bomb_radius, WIDTH - bomb_radius)
        bomb_y = -bomb_radius

    # Reset bomb if it falls off the screen
    if bomb_y > HEIGHT:
        bomb_x = random.randint(bomb_radius, WIDTH - bomb_radius)
        bomb_y = -bomb_radius

    # Draw basket
    pygame.draw.rect(screen, GREEN, (basket_x, basket_y, basket_width, basket_height))

    # Draw apple
    pygame.draw.circle(screen, RED, (apple_x, apple_y), apple_radius)

    # Draw bomb
    pygame.draw.circle(screen, BLUE, (bomb_x, bomb_y), bomb_radius)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, BLACK)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Check for game over
    if lives == 0:
        game_over_text = font.render("Game Over! Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.flip()

        # Wait for restart or quit
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    restart = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    score = 0
                    lives = 3
                    apple_speed = 5
                    apple_x = random.randint(apple_radius, WIDTH - apple_radius)
                    apple_y = -apple_radius
                    bomb_x = random.randint(bomb_radius, WIDTH - bomb_radius)
                    bomb_y = -bomb_radius
                    basket_x = WIDTH // 2 - basket_width // 2
                    restart = True

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
