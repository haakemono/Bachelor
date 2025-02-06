#renderlogic_py

import pygame
from constants import PLAYER_HEIGHT, PLAYER_WIDTH, WIDTH, HEIGHT, FONT, APPLE_RADIUS, BOMB_RADIUS

# Preload and scale images once to improve performance
background_image = pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT))
player_image = pygame.transform.scale(pygame.image.load("img/player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))
apple_image = pygame.transform.scale(pygame.image.load("img/apple.png"), (APPLE_RADIUS * 2, APPLE_RADIUS * 2))
bomb_image = pygame.transform.scale(pygame.image.load("img/bomb.png"), (BOMB_RADIUS * 2, BOMB_RADIUS * 2))

def draw_start_menu():
    WIN = pygame.display.get_surface()
    WIN.blit(background_image, (0, 0))

    title_text = FONT.render("Apple Catcher", True, "red")
    instruction_text = FONT.render ("Press SPACE to Start", True, "black")

    WIN.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
    WIN.blit(instruction_text, (WIDTH //2 - 120, HEIGHT // 2))

    pygame.display.flip()

def start_menu():
    while True:
        draw_start_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def pause_game():
    WIN = pygame.display.get_surface()
    paused = True

    while paused:
        WIN.blit(background_image, (0,0))
         
        pause_text = FONT.render("PAUSED", True, "white")
        resume_text = FONT.render ("Press P to Resume", True, "gray")

        WIN.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        WIN.blit(resume_text, (WIDTH // 2 - 100, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame. KEYDOWN and event.key == pygame.K_p:
                paused = False

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
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))

        WIN.blit(game_over_text, game_over_rect.topleft)

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
