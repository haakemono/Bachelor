import pygame
import os


pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
THIRD = SCREEN_WIDTH // 3
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Hub")

SELECTIONS = ["Gesture Hero", "Apple Catcher", "Chess"]
FONT = pygame.font.Font(None, 60)

images = [
    pygame.image.load("assets/gesture_hero.png"),
    pygame.image.load("assets/apple_catcher.png"),
    pygame.image.load("assets/chess.png")
]

def draw_hub(win, images, selected_index):
    win.fill((0, 0, 0))

    for i, img in enumerate(images):
        img = pygame.transform.scale(img, (THIRD, SCREEN_HEIGHT))
        x = i * THIRD
        if i == selected_index:
            win.blit(img, (x, 0))
            pygame.draw.rect(win, (255, 255, 255), (x, 0, THIRD, SCREEN_HEIGHT), 6)
        else:
            blurred = img.copy()
            s = pygame.Surface((THIRD, SCREEN_HEIGHT))
            s.set_alpha(150)
            s.fill((0, 0, 0))
            blurred.blit(s, (0, 0))
            win.blit(blurred, (x, 0))

    pygame.display.flip()

def run_gesture_hero():
    os.system("python3 gesture_hero/main.py")

def run_apple_catcher():
    os.system("python3 apple_catcher/main.py")

def run_chess():
    os.system("python3 chess/main.py")

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
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        run_gesture_hero()
                    elif selected_index == 1:
                        run_apple_catcher()
                    elif selected_index == 2:
                        run_chess()

        clock.tick(60)

if __name__ == "__main__":
    game_hub_loop()
    pygame.quit()
