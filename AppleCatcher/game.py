import pygame
import random
from hand_tracking import HandTracker
from render_logic import draw, reset_game
from constants import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, APPLE_RADIUS, BOMB_RADIUS, NEW_APPLE_INTERVAL, NEW_BOMB_INTERVAL, BOMB_FALL_SPEED, APPLE_FALL_SPEED

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
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_state = reset_game()  # Reset the game state

        if game_state["game_over"]:
            draw(game_state["player"], game_state["apples"], game_state["bombs"], game_state["score"], game_state["lives"], game_state["game_over"])
            continue

        player_x = hand_tracker.get_player_position()
        if player_x is not None:
            game_state["player"].x = WIDTH - player_x - game_state["player"].width // 2

        game_state["player"].x = max(0, min(WIDTH - PLAYER_WIDTH, game_state["player"].x))

        if game_state["frame_count"] % NEW_APPLE_INTERVAL == 0:
            apple_x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            game_state["apples"].append([apple_x, 0])

        if game_state["frame_count"] % NEW_BOMB_INTERVAL == 0:
            bomb_x = random.randint(BOMB_RADIUS, WIDTH - BOMB_RADIUS)
            game_state["bombs"].append([bomb_x, 0])

        game_state["apples"] = [(x, y + APPLE_FALL_SPEED) for x, y in game_state["apples"] if y + APPLE_RADIUS < HEIGHT]
        game_state["bombs"] = [(x, y + BOMB_FALL_SPEED) for x, y in game_state["bombs"] if y + BOMB_RADIUS < HEIGHT]

        player_rect = pygame.Rect(game_state["player"].x, game_state["player"].y, PLAYER_WIDTH, PLAYER_HEIGHT)
        for apple in game_state["apples"]:
            apple_rect = pygame.Rect(apple[0] - APPLE_RADIUS, apple[1] - APPLE_RADIUS, APPLE_RADIUS * 2, APPLE_RADIUS * 2)
            if player_rect.colliderect(apple_rect):
                game_state["score"] += 1
                game_state["apples"].remove(apple)

        # Handle bomb collisions
        for bomb in game_state["bombs"][:]:
            bomb_rect = pygame.Rect(bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS, BOMB_RADIUS * 2, BOMB_RADIUS * 2)
            if player_rect.colliderect(bomb_rect):
                game_state["lives"] -= 1
                game_state["bombs"].remove(bomb)
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True

        draw(game_state["player"], game_state["apples"], game_state["bombs"], game_state["score"], game_state["lives"], game_state["game_over"])

    hand_tracker.release()
    pygame.quit()
