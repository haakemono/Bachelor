# game_logic.py
import pygame
from constants import WIDTH, HEIGHT, FONT, APPLE_RADIUS, BOMB_RADIUS

def draw(player, apples, bombs, score, lives, game_over):
    WIN = pygame.display.get_surface()
    WIN.blit(pygame.transform.scale(pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT)), (0, 0))
    pygame.draw.rect(WIN, "brown", player)

    for apple in apples:
        pygame.draw.circle(WIN, "red", (apple[0], apple[1]), APPLE_RADIUS)
    
    for bomb in bombs:
        pygame.draw.circle(WIN, "blue", (bomb[0], bomb[1]), BOMB_RADIUS)

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
