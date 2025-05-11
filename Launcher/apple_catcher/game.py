import pygame
import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from shared_input.tracking import BallTracker, HandTracker
from render_logic import draw, reset_game, start_menu, pause_game
from constants import WIDTH, HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, APPLE_RADIUS, BOMB_RADIUS

use_handtracking = 1 #set to 0 for object (handball) tracking, set to 1 for finger tracking

def move_straight(objects, speed):
    return [(x, y + speed) for x, y in objects if y + APPLE_RADIUS < HEIGHT]

def move_diagonal(objects, speeds, directions):
    new_objects, new_directions = [], []
    for i, (x, y) in enumerate(objects):
        new_x, new_y = x + directions[i] * 5, y + speeds[i]
        if new_x - APPLE_RADIUS <= 0 or new_x + APPLE_RADIUS >= WIDTH:
            directions[i] *= -1
        new_objects.append((new_x, new_y))
        new_directions.append(directions[i])
    return new_objects, new_directions

def move_easy(game_state):
    game_state["apples"] = move_straight(game_state["apples"], 2)
    game_state["bombs"] = move_straight(game_state["bombs"], 3)

def move_intermediate(game_state):
    while len(game_state["apple_directions"]) < len(game_state["apples"]):
        game_state["apple_directions"].append(random.choice([-1, 1]))
    game_state["apples"], game_state["apple_directions"] = move_diagonal(
        game_state["apples"], [4] * len(game_state["apples"]), game_state["apple_directions"]
    )
    while len(game_state["bomb_directions"]) < len(game_state["bombs"]):
        game_state["bomb_directions"].append(random.choice([-1, 1]))
    game_state["bombs"], game_state["bomb_directions"] = move_diagonal(
        game_state["bombs"], [7] * len(game_state["bombs"]), game_state["bomb_directions"]
    )

def move_hard(game_state):
    while len(game_state["bomb_directions"]) < len(game_state["bombs"]):
        game_state["bomb_directions"].append(random.choice([-1, 1]))
    game_state["bombs"], game_state["bomb_directions"] = move_diagonal(
        game_state["bombs"], [7] * len(game_state["bombs"]), game_state["bomb_directions"]
    )
    game_state["apples"] = []  # Remove apples in hard mode

def game_loop():
    pygame.init()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Apples Catching")
    clock = pygame.time.Clock()
    difficulty = start_menu()
    print(f"Selected Difficulty: {difficulty}")  # Debugging print

    game_state = reset_game()
    game_state["start_time"] = pygame.time.get_ticks()  # Track start time
    print(f"Game Started! Initial Start Time: {game_state['start_time']}")  # Debugging print
    if use_handtracking == 1:
        hand_tracker = HandTracker(WIDTH, HEIGHT)
    else:
        hand_tracker = BallTracker(WIDTH)
    run = True

    while run:
        clock.tick(60)
        game_state["frame_count"] += 1
        player_x = None


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_state = reset_game()
                    game_state["start_time"] = pygame.time.get_ticks()
                    print(f"Game Restarted! New Start Time: {game_state['start_time']}")  # Debugging print
                elif event.key in [pygame.K_ESCAPE, pygame.K_q]:
                    run = False
                elif event.key == pygame.K_p:
                    pause_game()

        # **Always Define player_rect to Avoid Crashes**
        player_rect = pygame.Rect(game_state["player"].x, game_state["player"].y, PLAYER_WIDTH, PLAYER_HEIGHT)

        # **Score Calculation**
        if not game_state["game_over"]:  # Only update score if the game is still running
            if "use_obstacles" in difficulty:
                # Hard Mode: Score is survival time
                current_time = pygame.time.get_ticks()
                game_state["score"] = (current_time - game_state["start_time"]) // 1000
            else:
                # Easy/Intermediate Mode: Score increments on apple catch
                for apple in game_state["apples"][:]:
                    apple_rect = pygame.Rect(apple[0] - APPLE_RADIUS, apple[1] - APPLE_RADIUS, APPLE_RADIUS * 2, APPLE_RADIUS * 2)
                    if player_rect.colliderect(apple_rect):
                        game_state["score"] += 1
                        game_state["apples"].remove(apple)

        draw(
            game_state["player"],
            game_state["apples"],
            game_state["bombs"],
            game_state["score"],
            game_state["lives"],
            game_state["game_over"]
        )

        if game_state["game_over"]:
            continue  # Skip processing if game is over

        position = hand_tracker.get_player_position()

        if position is not None:
            # Always extract only the horizontal x-position as an integer
            player_x = position[0] if isinstance(position, tuple) else position

            if use_handtracking == 1:
                game_state["player"].x = WIDTH - player_x - game_state["player"].width // 2
            else:
                game_state["player"].x = player_x - game_state["player"].width // 2

            game_state["player"].x = max(0, min(WIDTH - PLAYER_WIDTH, game_state["player"].x))




        if game_state["frame_count"] % difficulty["apple_interval"] == 0 and difficulty["apple_interval"] is not None:
            apple_x = random.randint(APPLE_RADIUS, WIDTH - APPLE_RADIUS)
            game_state["apples"].append([apple_x, 0])
            game_state["apple_directions"].append(random.choice([-1, 1]) if "use_diagonal" in difficulty else 0)

        if game_state["frame_count"] % difficulty["bomb_interval"] == 0 and random.random() < difficulty["bomb_probability"]:
            bomb_x = random.randint(BOMB_RADIUS, WIDTH - BOMB_RADIUS)
            game_state["bombs"].append([bomb_x, 0])

        if "use_straight" in difficulty:
            move_easy(game_state)
        elif "use_diagonal" in difficulty:
            move_intermediate(game_state)
        elif "use_obstacles" in difficulty:
            move_hard(game_state)

        for bomb in game_state["bombs"][:]:
            bomb_rect = pygame.Rect(bomb[0] - BOMB_RADIUS, bomb[1] - BOMB_RADIUS, BOMB_RADIUS * 2, BOMB_RADIUS * 2)
            if player_rect.colliderect(bomb_rect):
                game_state["lives"] -= 1
                game_state["bombs"].remove(bomb)
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True

        draw(
            game_state["player"],
            game_state["apples"],
            game_state["bombs"],
            game_state["score"],
            game_state["lives"],
            game_state["game_over"]
        )

    hand_tracker.release()
    pygame.quit()

if __name__ == "__main__":
    game_loop()