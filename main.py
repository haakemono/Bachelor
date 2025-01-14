import sys
import time
import pygame

WIDTH = 1000
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apples and Oranges")

BG= pygame.transform.scale(pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT))

def draw():
    WIN.blit(BG, (0, 0))
    pygame.display.update()
def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw()

    pygame.quit()


if __name__ == "__main__":
    main()