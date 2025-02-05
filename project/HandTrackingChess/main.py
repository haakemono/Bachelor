import pygame
import os
import sys
import chess
from chessboard import ChessBoard
from utils import handle_game_over, initialize_game  # Import the function from utils.py
from engine import ChessEngine
from evaluation_bar import EvaluationBar
from hand_tracking import handle_player_turn
from Constants import ASSETS_PATH, SQUARE_SIZE, SCREEN_SIZE, BAR_WIDTH, HOVER_TIME_THRESHOLD, STOCKFISH_PATH

def draw_game_state(screen, chessboard, evaluation_bar, game_state):
    """Render the chessboard, highlights, evaluation bar, and other UI elements."""
    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the chessboard
    chessboard.draw(screen)

    # Highlight selected square and valid moves
    if game_state["selected_square"] is not None:
        selected_row, selected_col = 7 - chess.square_rank(game_state["selected_square"]), chess.square_file(game_state["selected_square"])
        pygame.draw.rect(
            screen,
            (255, 255, 0),
            pygame.Rect(selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            5,
        )
        for move in game_state["valid_moves"]:
            move_row, move_col = 7 - chess.square_rank(move), chess.square_file(move)
            pygame.draw.circle(
                screen,
                (0, 255, 0),
                (move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                10,
            )

    # Highlight the bot's last move
    if game_state["bot_last_move"]:
        from_square, to_square = game_state["bot_last_move"].from_square, game_state["bot_last_move"].to_square
        from_row, from_col = 7 - chess.square_rank(from_square), chess.square_file(from_square)
        to_row, to_col = 7 - chess.square_rank(to_square), chess.square_file(to_square)

        pygame.draw.rect(
            screen, (0, 0, 255),
            pygame.Rect(from_col * SQUARE_SIZE, from_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5
        )
        pygame.draw.rect(
            screen, (0, 0, 255),
            pygame.Rect(to_col * SQUARE_SIZE, to_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5
        )

    # Always draw the dot
    pygame.draw.circle(screen, (255, 0, 0), (game_state["smoothed_x"], game_state["smoothed_y"]), 15)

    # Draw the evaluation bar
    evaluation_bar.draw(game_state["evaluation_score"])

    # Display the evaluation score as a number
    font = pygame.font.Font(None, 36)
    eval_text = f"Eval: {game_state['evaluation_score']:.2f}"
    eval_surface = font.render(eval_text, True, (255, 255, 255))
    screen.blit(eval_surface, (SCREEN_SIZE + 10, SCREEN_SIZE // 2 - 20))

    # Update the display
    pygame.display.flip()

def initialize_game_state():
    """Initialize all game state variables."""
    return {
        "hover_start_time": None,
        "hovered_square": None,
        "selected_square": None,
        "valid_moves": [],
        "bot_last_move": None,
        "game_over": False,
        "player_turn": True,
        "smoothed_x": SCREEN_SIZE // 2,
        "smoothed_y": SCREEN_SIZE // 2,
        "alpha": 0.9,
        "last_hand_position": (SCREEN_SIZE // 2, SCREEN_SIZE // 2),
        "evaluation_score": 0,
    }

def main():
    screen, engine, chessboard, evaluation_bar, hand_tracker = initialize_game()
    game_state = initialize_game_state()
    running = True

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:  # ESC or Q to exit
                    print("🔙 Returning to menu...")
                    running = False  # Stop the game loop

        # If the game is over, display the result and stop processing moves
        if game_state["game_over"]:
            handle_game_over(screen, engine)
            continue

        # Handle the player's turn or the bot's turn
        if game_state["player_turn"]:
            game_state = handle_player_turn(hand_tracker, engine, game_state)
        else:
            game_state = engine.handle_bot_turn(game_state)

        # Draw the game state
        draw_game_state(screen, chessboard, evaluation_bar, game_state)

        clock.tick(30)

    # Clean up resources
    hand_tracker.release()
    pygame.quit()

    # **Return to Menu Instead of Fully Exiting**
    menu_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "menu.py")
    print(f"🔄 Returning to Menu: {menu_path}")

    os.execv(sys.executable, ["python", menu_path])  # Replace the chess process with the menu

if __name__ == "__main__":
    main()
