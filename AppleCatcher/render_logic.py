import pygame
from constants import PLAYER_HEIGHT, PLAYER_WIDTH, WIDTH, HEIGHT, FONT, APPLE_RADIUS, BOMB_RADIUS

def draw(player, apples, bombs, score, lives, game_over):
    WIN = pygame.display.get_surface()
    WIN.blit(pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT)), (0, 0))

    player_image = pygame.image.load("img/player.png")  
    player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

    WIN.blit(player_image, (player.x, player.y))  # Display the player at its position


    apple_image = pygame.image.load ("img/apple.png")
    bomb_image = pygame.image.load ("img/bomb.png")

    for apple in apples:
        apple_scaled = pygame.transform.scale(apple_image, (APPLE_RADIUS * 2, APPLE_RADIUS * 2))
        WIN.blit(apple_scaled, (apple[0] - APPLE_RADIUS, apple[1] - APPLE_RADIUS))
    
    for bomb in bombs:
        bomb_scaled = pygame.transform.scale(bomb_image, (BOMB_RADIUS * 2, BOMB_RADIUS * 2))
        WIN.blit(bomb_scaled, (bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS))

    if game_over:
        game_over_text = FONT.render("GAME OVER", True, "red")
        WIN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        pygame.display.update()

        reset_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
        pygame.draw.rect(WIN, "green", reset_button)
        reset_text = FONT.render("Press R to Reset", True, "white")
        WIN.blit(reset_text, (WIDTH // 2 - 45, HEIGHT // 2 + 10))
        pygame.display.update()
        return reset_button

    score_text = FONT.render(f"Score: {score}", True, "black")
    lives_text = FONT.render(f"Lives: {lives}", True, "black")
    WIN.blit(score_text, (10, 10))
    WIN.blit(lives_text, (10, 40))
    pygame.display.update()

def reset_game():
    return {
        "player": pygame.Rect(200, HEIGHT - 20, 100, 20),
        "apples": [],
        "bombs": [],
        "score": 0,
        "lives": 3,
        "frame_count": 0,
        "game_over": False,
    }
