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

#bomb
BOMB_RADIUS = 15
BOMB_FALL_SPEED = 4
NEW_BOMB_INTERVAL = 300


#font
pygame.font.init()
FONT = pygame.font.Font(None, 36)

def draw(player, apples, bombs, score, lives, game_over):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, "brown", player)

    for apple in apples:
        pygame.draw.circle(WIN, "red", (apple[0], apple[1]), APPLE_RADIUS)
    
    for bomb in bombs:
        pygame.draw.circle(WIN, "blue", (bomb[0], bomb[1]), BOMB_RADIUS)

    if game_over:
        #game over text
        game_over_text = FONT.render("GAME OVER", True, "red")
        WIN.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        pygame.display.update()

        #reset button
        reset_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
        pygame.draw.rect(WIN, "green", reset_button)
        reset_text = FONT.render("Reset", True, "white")
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
    "player": pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT),
        "apples": [],
        "bombs": [],
        "score": 0,
        "lives": 3,
        "frame_count": 0,
        "game_over": False,    
    }

def main():
    game_state = reset_game()

    while True:
        clock.tick(60)
        game_state["frame_count"] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state["game_over"] and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                reset_button = draw(
                    game_state["player"],
                    game_state["apples"],
                    game_state["bombs"],
                    game_state["score"],
                    game_state["lives"],
                    game_state["game_over"],
                )
                if reset_button.collidepoint(mouse_pos):
                    game_state = reset_game()

        if game_state["game_over"]:
            reset_button = draw(
                game_state["player"],
                game_state["apples"],
                game_state["bombs"],
                game_state["score"],
                game_state["lives"],
                game_state["game_over"],
            )
            continue

        keybinds = pygame.key.get_pressed()
        if keybinds[pygame.K_LEFT] or keybinds[pygame.K_a]:
            game_state["player"].x -= PLAYER_VEL
        if keybinds[pygame.K_RIGHT] or keybinds[pygame.K_d]:
            game_state["player"].x += PLAYER_VEL 

        # Keep player in bounds
        if game_state["player"].x < 0:
            game_state["player"].x = 0
        if game_state["player"].x > WIDTH - PLAYER_WIDTH:
            game_state["player"].x = WIDTH - PLAYER_WIDTH

        # Spawn new apples
        if game_state["frame_count"] % NEW_APPLE_INTERVAL == 0:
            apple_x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            game_state["apples"].append([apple_x, 0])  # Apple starts at top

        # Spawn new bombs
        if game_state["frame_count"] % NEW_BOMB_INTERVAL == 0:
            bomb_x = random.randint(BOMB_RADIUS, WIDTH - BOMB_RADIUS)
            game_state["bombs"].append([bomb_x, 0])  # Bomb starts at top

        # Move apples and bombs down
        for apple in game_state["apples"]:
            apple[1] += APPLE_FALL_SPEED
        for bomb in game_state["bombs"]:
            bomb[1] += BOMB_FALL_SPEED

        # Remove objects after they fall off screen
        game_state["apples"] = [apple for apple in game_state["apples"] if apple[1] < HEIGHT]
        game_state["bombs"] = [bomb for bomb in game_state["bombs"] if bomb[1] < HEIGHT]

        # Check for apple collisions
        for apple in game_state["apples"][:]:
            if (
                game_state["player"].x < apple[0] < game_state["player"].x + PLAYER_WIDTH
                and game_state["player"].y < apple[1] + APPLE_RADIUS < game_state["player"].y + PLAYER_HEIGHT
            ):
                game_state["score"] += 1  # Increment score
                game_state["apples"].remove(apple)

        # Check for bomb collisions
        for bomb in game_state["bombs"][:]:
            if (
                game_state["player"].x < bomb[0] < game_state["player"].x + PLAYER_WIDTH
                and game_state["player"].y < bomb[1] + BOMB_RADIUS < game_state["player"].y + PLAYER_HEIGHT
            ):
                game_state["lives"] -= 1  # Decrement lives
                game_state["bombs"].remove(bomb)
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True

        draw(
            game_state["player"],
            game_state["apples"],
            game_state["bombs"],
            game_state["score"],
            game_state["lives"],
            game_state["game_over"],
        )


if __name__ == "__main__":
    main()