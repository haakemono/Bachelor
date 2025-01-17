import sys
import pygame
from logic import reset_game, spawn_object, update_objects, handle_collisions
from render import draw_window, draw_fps
from constants import WIDTH, HEIGHT, FPS, APPLE_RADIUS, BOMB_RADIUS
from hand_tracking import HandTracker
from difficulty_manager import DifficultyManager  # Ensure this line is present


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

    # Initialize DifficultyManager
    difficulty_manager = DifficultyManager()

    try:
        while True:
            clock.tick(FPS)
            game_state["frame_count"] += 1

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    hand_tracker.release()
                    sys.exit()

            # Check if the game is over
            if game_state["game_over"]:
                font_game_over = pygame.font.Font(None, 72)
                game_over_text = font_game_over.render("GAME OVER", True, "red")
                WIN.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        hand_tracker.release()
                        sys.exit()
                continue

            # Update basket position based on hand tracking
            basket_x = hand_tracker.get_basket_position()
            if basket_x is not None:
                game_state["player"].x = basket_x - game_state["player"].width // 2

            game_state["player"].x = max(0, min(WIDTH - game_state["player"].width, game_state["player"].x))

            # Get current game parameters
            params = difficulty_manager.get_game_parameters()
            apple_fall_speed = params["apple_fall_speed"]
            new_apple_interval = params["new_apple_interval"]
            new_bomb_interval = params["new_bomb_interval"]

            # Game logic
            if game_state["frame_count"] % new_apple_interval == 0:
                spawn_object(game_state["apples"], APPLE_RADIUS, game_state)

            if game_state["frame_count"] % new_bomb_interval == 0:
                spawn_object(game_state["bombs"], BOMB_RADIUS)

            update_objects(
                game_state["apples"],
                apple_fall_speed,
                game_state,
                difficulty_manager
            )
            update_objects(
                game_state["bombs"],
                4  # Bomb fall speed
            )

            handle_collisions(
                game_state["apples"],
                game_state["player"],
                game_state,
                difficulty_manager,
                score_increment=1,
                life_decrement=0,
            )
            handle_collisions(
                game_state["bombs"],
                game_state["player"],
                game_state,
                difficulty_manager=None,  # No performance tracking for bombs
                score_increment=0,
                life_decrement=1,
            )

            # Adjust difficulty every few frames
            if game_state["frame_count"] % (FPS * 2) == 0:  # Every 2 seconds
                difficulty_manager.adjust_difficulty()

            # Render game
            true_score = game_state["true_score"]
            score = game_state["score"]
            accuracy = (score / true_score * 100) if true_score > 0 else 0
            draw_window(
                WIN,
                BG,
                game_state["player"],
                game_state["apples"],
                game_state["bombs"],
                score,
                true_score,
                accuracy,
                game_state["lives"],
            )
            draw_fps(WIN, clock, font)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        hand_tracker.release()
        pygame.quit()

if __name__ == "__main__":
    main()
