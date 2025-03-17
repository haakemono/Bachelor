import pygame
import subprocess

WIDTH, HEIGHT = 640, 480

def run_main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Game Launcher - Main Menu")

    font = pygame.font.SysFont(None, 36)

    buttons = {
        "Apple Catcher": pygame.Rect(200, 120, 240, 50),
        "Gesture Hero": pygame.Rect(200, 200, 240, 50),
        "Chess Game": pygame.Rect(200, 280, 240, 50),
        "Exit": pygame.Rect(200, 360, 240, 50),
    }

    clock = pygame.time.Clock()
    while True:
        screen.fill((25, 25, 25))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        if name == "Apple Catcher":
                            subprocess.Popen(["python", "games/AppleCatcher/main.py"])
                        elif name == "Gesture Hero":
                            subprocess.Popen(["python", "games/GestureHero/main.py"])
                        elif name == "Chess Game":
                            subprocess.Popen(["python", "games/ny_sjakk/main.py"])
                        elif name == "Exit":
                            pygame.quit()
                            exit()

        for name, rect in buttons.items():
            pygame.draw.rect(screen, (70, 130, 180), rect)
            text = font.render(name, True, (255, 255, 255))
            screen.blit(text, (rect.x + (rect.width - text.get_width()) // 2, rect.y + 10))

        pygame.display.flip()
        clock.tick(30)