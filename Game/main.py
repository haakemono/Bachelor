import sys
import pygame
from logic import reset_game, spawn_object, update_objects, handle_collisions
from render import draw_window, draw_fps
from constants import WIDTH, HEIGHT, FPS, APPLE_RADIUS, BOMB_RADIUS
from hand_tracking import HandTracker

# Initialize Pygame
pygame.init()  # Initialize all Pygame modules

# Pygame setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apples and Oranges")
BG = pygame.transform.scale(pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT))
clock = pygame.time.Clock()

def main():
    # Initialize game state
    game_state = reset_game()

    # Font for FPS counter
    font = pygame.font.Font(None, 36)

    # Initialize HandTracker
    hand_tracker = HandTracker(WIDTH)

    try:
        while True:
            clock.tick(FPS)
            game_state["frame_count"] += 1

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    hand_tracker.release()  # Release camera resources
                    sys.exit()

            # Update basket position based on hand tracking
            basket_x = hand_tracker.get_basket_position()
            if basket_x is not None:
                game_state["player"].x = basket_x - game_state["player"].width // 2  # Center basket under hand

            # Ensure basket stays within bounds
            game_state["player"].x = max(0, min(WIDTH - game_state["player"].width, game_state["player"].x))

            # Game logic
            if game_state["frame_count"] % 180 == 0:
                spawn_object(game_state["apples"], APPLE_RADIUS)

            if game_state["frame_count"] % 300 == 0:
                spawn_object(game_state["bombs"], BOMB_RADIUS)

            update_objects(game_state["apples"], 3)  # Apple fall speed
            update_objects(game_state["bombs"], 4)  # Bomb fall speed

            handle_collisions(game_state["apples"], game_state["player"], game_state, score_increment=1, life_decrement=0)
            handle_collisions(game_state["bombs"], game_state["player"], game_state, score_increment=0, life_decrement=1)

            # Render game
            draw_window(WIN, BG, game_state["player"], game_state["apples"], game_state["bombs"], game_state["score"], game_state["lives"])
            draw_fps(WIN, clock, font)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        hand_tracker.release()  # Ensure camera resources are released
        pygame.quit()


if __name__ == "__main__":
    main()
