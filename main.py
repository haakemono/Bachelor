import sys
import time
import pygame
import random

WIDTH = 1000
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apples and Oranges")

BG= pygame.transform.scale(pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT))

#frames
clock = pygame.time.Clock()

#time
start_time = time.time()

#player
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20
PLAYER_VEL = 10

#apple
APPLE_RADIUS = 15
APPLE_FALL_SPEED = 3
NEW_APPLE_INTERVAL = 180

def draw(player, apples):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, "brown", player)
    for apple in apples:
        pygame.draw.circle(WIN, "red", (apple[0], apple[1]), APPLE_RADIUS)
    pygame.display.update()
def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    apples = []
    frame_count = 0 #init frame_count

    while run:
        clock.tick(60)

        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keybinds = pygame.key.get_pressed()
        if keybinds[pygame.K_LEFT] or keybinds[pygame.K_a]:
            player.x -= PLAYER_VEL
        if keybinds[pygame.K_RIGHT] or keybinds[pygame.K_d]:
            player.x += PLAYER_VEL 

        if player.x <0:
            player.x= 0
        if player.x > WIDTH - PLAYER_WIDTH:
            player.x = WIDTH - PLAYER_WIDTH

        if frame_count % NEW_APPLE_INTERVAL == 0:
            apple_x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            apples.append([apple_x, 0]) #apple starts at top
        for apple in apples:
            apple[1] += APPLE_FALL_SPEED #move apple down

        #remove apples after fall off screen
        apples = [apple for apple in apples if apple[1] < HEIGHT] 

        #check for collisions
        for apple in apples:
            if (player.x < apple[0] < player.x + PLAYER_WIDTH and
                player.y < apple [1] + APPLE_RADIUS < player.y + PLAYER_HEIGHT):
                print ("Caught an apple!") #Increment score
                apples.remove(apple)

        draw(player, apples)
   


    pygame.quit()


if __name__ == "__main__":
    main()