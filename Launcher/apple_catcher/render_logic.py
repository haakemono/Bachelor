import os
import pygame
from constants import PLAYER_HEIGHT, PLAYER_WIDTH, WIDTH, HEIGHT, FONT, APPLE_RADIUS, BOMB_RADIUS

# Dynamically resolve the image directory
BASE_PATH = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_PATH, "img")

# Correct image loading with paths
background_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "background.png")), (WIDTH, HEIGHT)
)
player_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "player.png")), (PLAYER_WIDTH, PLAYER_HEIGHT)
)
apple_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "apple.png")), (APPLE_RADIUS * 2, APPLE_RADIUS * 2)
)
bomb_image = pygame.transform.scale(
    pygame.image.load(os.path.join(IMG_PATH, "bomb.png")), (BOMB_RADIUS * 2, BOMB_RADIUS * 2)
)

def draw_start_menu(selected_index):
    WIN = pygame.display.get_surface()
    WIN.blit(background_image, (0, 0))
    title_text = FONT.render("Apple Catcher", True, "red")
    instruction_text = FONT.render("Press SPACE to Start", True, "black")
    WIN.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 140))
    WIN.blit(instruction_text, (WIDTH // 2 - 120, HEIGHT // 2 - 100))
    difficulties = ["Easy", "Normal", "Hard"]
    for i, difficulty in enumerate(difficulties):
        color = "yellow" if i == selected_index else "white"
        difficulty_text = FONT.render(difficulty, True, color)
        WIN.blit(difficulty_text, (WIDTH // 2 - 50, HEIGHT // 2 + i * 40))
    pygame.display.flip()

def start_menu():
    selected_index = 1
    difficulties = {
        "Easy": {"fall_speed": 2, "apple_interval": 80, "bomb_interval": 100, "bomb_probability": 0.1, "use_straight": True},
        "Intermediate": {"fall_speed": 4, "apple_interval": 60, "bomb_interval": 70, "bomb_probability": 0.3, "use_diagonal": True},
        "Hard": {"fall_speed": 6, "apple_interval": float('inf'), "bomb_interval": 20, "bomb_probability": 0.8, "use_diagonal": True, "use_obstacles": True}
    }
    while True:
        draw_start_menu(selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % 3
                elif event.key == pygame.K_SPACE:
                    return difficulties[list(difficulties.keys())[selected_index]]

def pause_game():
    WIN = pygame.display.get_surface()
    paused = True
    while paused:
        WIN.blit(background_image, (0, 0))
        pause_text = FONT.render("PAUSED", True, "white")
        resume_text = FONT.render("Press P to Resume", True, "gray")
        WIN.blit(pause_text, (WIDTH // 2 - 50, HEIGHT // 2 - 50))
        WIN.blit(resume_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

def draw(player, apples, bombs, score, lives, game_over):
    WIN = pygame.display.get_surface()
    WIN.blit(background_image, (0, 0))
    WIN.blit(player_image, (player.x, player.y))
    for apple in apples:
        WIN.blit(apple_image, (apple[0] - APPLE_RADIUS, apple[1] - APPLE_RADIUS))
    for bomb in bombs:
        WIN.blit(bomb_image, (bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS))
    if game_over:
        game_over_text = FONT.render("GAME OVER", True, "red")
        WIN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 80))
        reset_text = FONT.render("Press R to Reset", True, "white")
        WIN.blit(reset_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    WIN.blit(FONT.render(f"Score: {score}", True, "black"), (10, 10))
    WIN.blit(FONT.render(f"Lives: {lives}", True, "black"), (10, 40))
    pygame.display.flip()

def reset_game():
    difficulty = start_menu()
    return {
        "player": pygame.Rect(200, HEIGHT - 20, PLAYER_WIDTH, PLAYER_HEIGHT),
        "apples": [],
        "bombs": [],
        "apple_directions": [],
        "bomb_directions": [],
        "score": 0,
        "lives": 3,
        "frame_count": 0,
        "game_over": False,
    }