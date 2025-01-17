import sys
import pygame
from difficulty_manager import DifficultyManager
from hand_tracking import HandTracker
from game_logic import GameLogic

# Pygame setup
WIDTH = 1000
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apples and Oranges")
BG = pygame.transform.scale(pygame.image.load("img/background.jpg"), (WIDTH, HEIGHT))

# Frames
clock = pygame.time.Clock()

# Font
pygame.font.init()
FONT = pygame.font.Font(None, 36)


def main():
    # Initialize components
    game_logic = GameLogic(WIDTH, HEIGHT, FONT)
    difficulty_manager = DifficultyManager()
    hand_tracker = HandTracker(WIDTH)

    # Initialize game state
    game_state = game_logic.reset_game()

    try:
        while True:
            clock.tick(60)
            game_state["frame_count"] += 1

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    hand_tracker.release()
                    sys.exit()

            # Get basket position from hand tracking
            basket_x = hand_tracker.get_basket_position()
            if basket_x is not None:
                game_state["player"].x = basket_x - 50  # Center the basket around the wrist

            # Constrain player within bounds
            game_state["player"].x = max(0, min(WIDTH - 100, game_state["player"].x))

            # Get current game parameters
            params = difficulty_manager.get_game_parameters()
            apple_fall_speed = params["apple_fall_speed"]
            new_apple_interval = params["new_apple_interval"]
            new_bomb_interval = params["new_bomb_interval"]

            # Spawn apples and bombs
            if game_state["frame_count"] % new_apple_interval == 0:
                game_logic.spawn_apple(game_state["apples"])
                difficulty_manager.track_performance()  # Track apple spawn

            if game_state["frame_count"] % new_bomb_interval == 0:
                game_logic.spawn_bomb(game_state["bombs"])

            # Update apples and bombs
            game_logic.update_objects(game_state["apples"], game_state["bombs"], apple_fall_speed)

            # Check for collisions
            game_logic.check_collisions(game_state, difficulty_manager)

            # Adjust difficulty every few frames
            if game_state["frame_count"] % 600 == 0:
                difficulty_manager.adjust_difficulty()

            # Draw the game state
            game_logic.draw(
                WIN,
                BG,
                game_state["player"],
                game_state["apples"],
                game_state["bombs"],
                game_state["score"],
                game_state["lives"],
                game_state["game_over"],
            )

    finally:
        hand_tracker.release()


if __name__ == "__main__":
    main()
