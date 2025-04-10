import sys
import pygame
import os

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
TOP_IMAGE_WIDTH = SCREEN_WIDTH // 3
TOP_IMAGE_HEIGHT = 600
BOTTOM_IMAGE_HEIGHT = SCREEN_HEIGHT - TOP_IMAGE_HEIGHT

WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Hub")

SELECTIONS = ["Gesture Hero", "Apple Catcher", "Chess", "Draw Game"]
FONT = pygame.font.Font(None, 60)

images = [
    pygame.image.load("assets/gesture_hero.png"),
    pygame.image.load("assets/apple_catcher.png"),
    pygame.image.load("assets/chess.png"),
    pygame.image.load("assets/draw_game.png")
]

def draw_hub(win, images, selected_index):
    win.fill((0, 0, 0))

    # Draw top 3 games
    for i in range(3):
        img = pygame.transform.scale(images[i], (TOP_IMAGE_WIDTH, TOP_IMAGE_HEIGHT))
        x = i * TOP_IMAGE_WIDTH
        y = 0

        if selected_index == i:
            win.blit(img, (x, y))
            pygame.draw.rect(win, (255, 255, 255), (x, y, TOP_IMAGE_WIDTH, TOP_IMAGE_HEIGHT), 6)
        else:
            blurred = img.copy()
            s = pygame.Surface((TOP_IMAGE_WIDTH, TOP_IMAGE_HEIGHT))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            blurred.blit(s, (0, 0))
            win.blit(blurred, (x, y))

    draw_game_index = 3
    img = pygame.transform.scale(images[draw_game_index], (SCREEN_WIDTH, BOTTOM_IMAGE_HEIGHT))
    y = TOP_IMAGE_HEIGHT
    if selected_index == draw_game_index:
        win.blit(img, (0, y))
        pygame.draw.rect(win, (255, 255, 255), (0, y, SCREEN_WIDTH, BOTTOM_IMAGE_HEIGHT), 6)
    else:
        blurred = img.copy()
        s = pygame.Surface((SCREEN_WIDTH, BOTTOM_IMAGE_HEIGHT))
        s.set_alpha(150)
        s.fill((0, 0, 0))
        blurred.blit(s, (0, 0))
        win.blit(blurred, (0, y))

    pygame.display.flip()

def run_gesture_hero():
    os.system(f"{sys.executable} gesture_hero/main.py")

def run_apple_catcher():
    os.system(f"{sys.executable} apple_catcher/main.py")

def run_chess():
    os.system(f"{sys.executable} chess/main.py")

def run_draw_game():
    os.system(f"{sys.executable} draw_game/draw_game.py")

def game_hub_loop():
    selected_index = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        draw_hub(WIN, images, selected_index)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
         
                if selected_index < 3:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % 3
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % 3

     
                if event.key == pygame.K_DOWN and selected_index < 3:
                    selected_index = 3
                elif event.key == pygame.K_UP and selected_index == 3:
                    selected_index = 0

                
                if event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        run_gesture_hero()
                    elif selected_index == 1:
                        run_apple_catcher()
                    elif selected_index == 2:
                        run_chess()
                    elif selected_index == 3:
                        run_draw_game()

        clock.tick(60)

if __name__ == "__main__":
    game_hub_loop()
    pygame.quit()
