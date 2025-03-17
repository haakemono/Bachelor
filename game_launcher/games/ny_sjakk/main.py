import pygame
import chess
from chessboard import ChessBoard
from engine import ChessEngine
from evaluation_bar import EvaluationBar
from gesture_recognition import GestureRecognizer
import time

import os

BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")

SQUARE_SIZE = 80
SCREEN_SIZE = SQUARE_SIZE * 8
BAR_WIDTH = 20

def evaluate_board(engine):
    """
    A basic evaluation function that calculates the material balance.
    Positive for white, negative for black.

    Args:
        engine (ChessEngine): The chess engine instance.

    Returns:
        float: The evaluation score.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  # The King has no evaluation value.
    }

    evaluation = 0
    for square in chess.SQUARES:
        piece = engine.board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            evaluation += value if piece.color else -value
    return evaluation

def highlight_square(screen, file, rank, color, thickness=5):
    """
    Highlights a square on the board with a specified color and thickness.

    Args:
        screen (pygame.Surface): The surface to draw on.
        file (int): The column index (0-7).
        rank (int): The row index (0-7).
        color (tuple): The color to highlight the square with.
        thickness (int): The thickness of the highlight border.
    """
    pygame.draw.rect(
        screen,
        color,  # Highlight color
        pygame.Rect(file * SQUARE_SIZE, (7 - rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
        thickness
    )

def draw_valid_moves(screen, valid_moves):
    """
    Draws red dots on valid move squares.
    
    Args:
        screen (pygame.Surface): The surface to draw on.
        valid_moves (list): List of valid move squares (each a tuple of (file, rank)).
    """
    for move in valid_moves:
        valid_file, valid_rank = move
        # Draw a small red dot on valid move squares
        pygame.draw.circle(
            screen,
            (255, 0, 0),  # Red color
            (valid_file * SQUARE_SIZE + SQUARE_SIZE // 2, (7 - valid_rank) * SQUARE_SIZE + SQUARE_SIZE // 2),
            10  # Radius of the dot
        )

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE + 30))
    pygame.display.set_caption("Chess")

    stockfish_path = r"C:\Users\haako\OneDrive\Documents\Skole\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
    engine = ChessEngine(stockfish_path)
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)
    gesture_recognizer = GestureRecognizer()

    # Hardcoded difficulty selection
    selected_difficulty = "easy"  # Change this to "medium" or "hard" if you want different difficulty
    print(f"Difficulty selected: {selected_difficulty}")

    # Game variables
    selected_file = None
    selected_rank = None
    target_file = None
    target_rank = None
    selecting = "file"
    selected_piece_square = None
    valid_moves = []  # To store the valid moves to highlight

    clock = pygame.time.Clock()

    # Game loop
    while True:
        screen.fill((0, 0, 0))
        chessboard.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                engine.close()  # Close Stockfish engine
                return

        # Draw valid move dots while waiting for destination selection
        draw_valid_moves(screen, valid_moves)

        # Get gestures for chess moves only after difficulty is selected
        gesture = gesture_recognizer.get_move_gesture()  # Get move-related gesture

        # Player's Move (white)
        if engine.turn == "white" and gesture:  # Only proceed if a valid gesture is detected
            print(f"Captured gesture: {gesture}")
            if selecting == "file":
                while True:
                    if gesture in gesture_recognizer.gesture_to_file:
                        selected_file = gesture_recognizer.gesture_to_file[gesture]
                        print(f"Selected Column: {chr(ord('A') + selected_file)}")

                        # Highlight the selected column in yellow
                        pygame.draw.rect(
                            screen,
                            (255, 255, 0, 100),  # Yellow column highlight
                            pygame.Rect(selected_file * SQUARE_SIZE, 0, SQUARE_SIZE, SCREEN_SIZE),
                            0
                        )
                        pygame.display.flip()
                        selecting = "rank"
                        break

            elif selecting == "rank":
                while True:
                    if gesture in gesture_recognizer.gesture_to_rank:
                        selected_rank = gesture_recognizer.gesture_to_rank[gesture]
                        print(f"Selected Row: {selected_rank + 1}")

                        # Highlight the selected square with the piece in yellow
                        pygame.draw.rect(
                            screen,
                            (255, 255, 0, 100),  # Yellow row highlight
                            pygame.Rect(selected_file * SQUARE_SIZE, (7 - selected_rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                            5
                        )
                        pygame.display.flip()
                        selected_square = chess.square(selected_file, selected_rank)
                        piece = engine.board.piece_at(selected_square)

                        if piece is None or piece.color != engine.board.turn:
                            selecting = "file"
                            time.sleep(2)
                            break

                        # Highlight the possible moves of the selected piece
                        possible_moves = engine.get_valid_moves(selected_square)
                        valid_moves = [(chess.square_file(move), chess.square_rank(move)) for move in possible_moves]  # Update valid moves

                        selected_piece_square = selected_square  # Remember the selected piece square
                        selecting = "target_file"
                        break

            elif selecting == "target_file":
                if gesture in gesture_recognizer.gesture_to_file:
                    target_file = gesture_recognizer.gesture_to_file[gesture]
                    print(f"Locked Destination Column: {chr(ord('A') + target_file)}")

                    # Highlight the destination column in red
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0, 100),  # Red column highlight
                        pygame.Rect(target_file * SQUARE_SIZE, 0, SQUARE_SIZE, SCREEN_SIZE),
                        0
                    )
                    pygame.display.flip()
                    selecting = "target_rank"
                    time.sleep(3)

            elif selecting == "target_rank":
                if gesture in gesture_recognizer.gesture_to_rank:
                    target_rank = gesture_recognizer.gesture_to_rank[gesture]
                    print(f"Locked Destination Row: {target_rank + 1}")

                    # Highlight the destination square in red
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),  # Red square highlight
                        pygame.Rect(target_file * SQUARE_SIZE, (7 - target_rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        5
                    )
                    pygame.display.flip()
                    time.sleep(3)

                    start_square = chess.square(selected_file, selected_rank)
                    end_square = chess.square(target_file, target_rank)
                    move = chess.Move(from_square=start_square, to_square=end_square)

                    if move in engine.board.legal_moves:
                        engine.make_move(move.uci())
                        print(f"Player's move: {move.uci()}")

                        # Switch turn after valid move
                        engine.turn = "black"  # Now it should be black's turn (AI)

                        # Reset selection variables after player move
                        selected_file = None
                        selected_rank = None
                        target_file = None
                        target_rank = None
                        selected_piece_square = None
                        valid_moves = []  # Clear valid moves
                        selecting = "file"

                        if engine.is_game_over():
                            print("Game Over!")
                            return

                    else:
                        print("Invalid move: This is not a legal move. Please try again.")
                        selected_file = None
                        selected_rank = None
                        target_file = None
                        target_rank = None
                        selecting = "file"
                        time.sleep(2)

        # AI's Move (black)
        if engine.turn == "black" and not gesture:  # Only let the AI move if it's its turn and no gesture
            print("AI is thinking...")
            ai_move = engine.ai_move(difficulty=selected_difficulty)  # Pass selected difficulty here
            print(f"AI Move: {ai_move}")

            # After AI moves, switch turn back to player (white)
            engine.turn = "white"  # Now it's the player's turn again

            # Reset selection variables after AI move
            selected_file = None
            selected_rank = None
            target_file = None
            target_rank = None
            selected_piece_square = None
            selecting = "file"

            if engine.is_game_over():
                print("Game Over!")
                return

        # Draw evaluation bar
        evaluation = evaluate_board(engine)
        evaluation_bar.draw(evaluation)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()