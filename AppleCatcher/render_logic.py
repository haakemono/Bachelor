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
        WIN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        reset_button_width = 220
        reset_button_height = 60
        reset_button_x = WIDTH // 2 - reset_button_width // 2
        reset_button_y = HEIGHT // 2 + 20
    
        pygame.draw.rect(WIN, "black", (reset_button_x, reset_button_y, reset_button_width, reset_button_height))

        reset_text = FONT.render("Press R to Reset", True, "white")
        text_rect = reset_text.get_rect(center=(reset_button_x + reset_button_width // 2, reset_button_y + reset_button_height // 2))
        WIN.blit(reset_text, text_rect.topleft)


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
        "lives": 1,
        "frame_count": 0,
        "game_over": False,
    }
