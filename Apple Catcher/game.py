# game.py
import pygame
import random
from hand_tracking import HandTracker
from logic import draw, reset_game
from constants import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, APPLE_RADIUS, BOMB_RADIUS, NEW_APPLE_INTERVAL, NEW_BOMB_INTERVAL,  BOMB_FALL_SPEED, APPLE_FALL_SPEED

def game_loop():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Apples Catching")
    clock = pygame.time.Clock()

    # Initialize game state
    game_state = reset_game()

    hand_tracker = HandTracker(WIDTH)

    run = True
    while run:
        clock.tick(60)
        game_state["frame_count"] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = reset_game()  # Reset the game state

        if game_state["game_over"]:
            draw(game_state["player"], game_state["apples"], game_state["bombs"], game_state["score"], game_state["lives"], game_state["game_over"])
            continue

        # Get player position using HandTracker
        player_x = hand_tracker.get_player_position()
        if player_x is not None:
            game_state["player"].x = WIDTH - player_x - game_state["player"].width // 2


        # Keep player within screen bounds
        if game_state["player"].x < 0:
            game_state["player"].x = 0
        if game_state["player"].x > WIDTH - PLAYER_WIDTH:
            game_state["player"].x = WIDTH - PLAYER_WIDTH

        if game_state["frame_count"] % NEW_APPLE_INTERVAL == 0:
            apple_x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            game_state["apples"].append([apple_x, 0])

        if game_state["frame_count"] % NEW_BOMB_INTERVAL == 0:
            bomb_x = random.randint(BOMB_RADIUS, WIDTH - BOMB_RADIUS)
            game_state["bombs"].append([bomb_x, 0])

        for apple in game_state["apples"]:
            apple[1] += APPLE_FALL_SPEED
        for bomb in game_state["bombs"]:
            bomb[1] += BOMB_FALL_SPEED

        game_state["apples"] = [apple for apple in game_state["apples"] if apple[1] < HEIGHT]
        game_state["bombs"] = [bomb for bomb in game_state["bombs"] if bomb[1] < HEIGHT]

        for apple in game_state["apples"]:
            if (game_state["player"].x < apple[0] < game_state["player"].x + PLAYER_WIDTH and
                game_state["player"].y < apple[1] + APPLE_RADIUS < game_state["player"].y + PLAYER_HEIGHT):
                game_state["score"] += 1
                game_state["apples"].remove(apple)

        for bomb in game_state["bombs"][:]:
            if (game_state["player"].x < bomb[0] < game_state["player"].x + PLAYER_WIDTH and
                game_state["player"].y < bomb[1] + BOMB_RADIUS < game_state["player"].y + PLAYER_HEIGHT):
                game_state["lives"] -= 1
                game_state["bombs"].remove(bomb)
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True

        draw(game_state["player"], game_state["apples"], game_state["bombs"], game_state["score"], game_state["lives"], game_state["game_over"])

    hand_tracker.release()
    pygame.quit()
