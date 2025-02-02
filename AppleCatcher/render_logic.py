import pygame
from constants import PLAYER_HEIGHT, PLAYER_WIDTH, WIDTH, HEIGHT, FONT, APPLE_RADIUS, BOMB_RADIUS

# Preload and scale images once to improve performance
background_image = pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT))
player_image = pygame.transform.scale(pygame.image.load("img/player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
apple_image = pygame.transform.scale(pygame.image.load("img/apple.png"), (APPLE_RADIUS * 2, APPLE_RADIUS * 2))
bomb_image = pygame.transform.scale(pygame.image.load("img/bomb.png"), (BOMB_RADIUS * 2, BOMB_RADIUS * 2))

def draw(player, apples, bombs, score, lives, game_over):
    WIN = pygame.display.get_surface()
    WIN.blit(background_image, (0, 0))

    # Draw player
    WIN.blit(player_image, (player.x, player.y))

    # Draw apples
    for apple in apples:
        WIN.blit(apple_image, (apple[0] - APPLE_RADIUS, apple[1] - APPLE_RADIUS))
    
    # Draw bombs
    for bomb in bombs:
        WIN.blit(bomb_image, (bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS))

    if game_over:
        game_over_text = FONT.render("GAME OVER", True, "red")
        WIN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))

        reset_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
        pygame.draw.rect(WIN, "green", reset_button)
        reset_text = FONT.render("Press R to Reset", True, "white")
        WIN.blit(reset_text, (WIDTH // 2 - 45, HEIGHT // 2 + 10))

    # Display score and lives
    score_text = FONT.render(f"Score: {score}", True, "black")
    lives_text = FONT.render(f"Lives: {lives}", True, "black")
    WIN.blit(score_text, (10, 10))
    WIN.blit(lives_text, (10, 40))

    # Use a single display update per frame
    pygame.display.flip()

def reset_game():
    return {
        "player": pygame.Rect(200, HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT),
        "apples": [],
        "bombs": [],
        "score": 0,
        "lives": 3,
        "frame_count": 0,
        "game_over": False,
    }
