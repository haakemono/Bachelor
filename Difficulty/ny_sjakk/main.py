import pygame
import chess
from chessboard import ChessBoard
from engine import ChessEngine
from evaluation_bar import EvaluationBar
from gesture_recognition import GestureRecognizer
import time

# Constants
ASSETS_PATH = "assets"
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE + 30))  # Increased height for column labels
    pygame.display.set_caption("Chess")

    engine = ChessEngine()
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)
    gesture_recognizer = GestureRecognizer()

    selected_file = None
    selected_rank = None
    target_file = None
    target_rank = None
    selecting = "file"  # Tracks the current selection step

    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        chessboard.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        gesture = gesture_recognizer.get_gesture()

        if gesture:
            if selecting == "file":
                while True:  # Keep looping until a valid piece is selected
                    if gesture in gesture_recognizer.gesture_to_file:
                        selected_file = gesture_recognizer.gesture_to_file[gesture]
                        print(f"Locked Column: {chr(ord('A') + selected_file)}")

                        # Highlight selected column in yellow
                        pygame.draw.rect(
                            screen,
                            (255, 255, 0, 100),  # Yellow column highlight
                            pygame.Rect(selected_file * SQUARE_SIZE, 0, SQUARE_SIZE, SCREEN_SIZE),
                            0
                        )
                        pygame.display.flip()

                        time.sleep(3)

                        selecting = "rank"
                        break  # Exit loop and move to row selection

                    gesture = gesture_recognizer.get_gesture()  # Wait for a new valid gesture

            elif selecting == "rank":
                while True:  # Keep looping until a valid piece is selected
                    if gesture in gesture_recognizer.gesture_to_rank:
                        selected_rank = gesture_recognizer.gesture_to_rank[gesture]
                        selected_square = chess.square(selected_file, selected_rank)
                        piece = engine.board.piece_at(selected_square)

                        # **Validate Selection**
                        if piece is None:
                            print("Invalid selection: No piece on this square. Please select again.")
                            selecting = "file"
                            time.sleep(2)
                            break  # Restart selection process

                        if piece.color != engine.board.turn:
                            print("Invalid selection: You must select your own piece. Please select again.")
                            selecting = "file"
                            time.sleep(2)
                            break  # Restart selection process

                        print(f"Locked Row: {selected_rank + 1}")

                        # Highlight selected square with yellow border
                        pygame.draw.rect(
                            screen,
                            (255, 255, 0),  # Yellow outline
                            pygame.Rect(selected_file * SQUARE_SIZE, (7 - selected_rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                            5
                        )
                        pygame.display.flip()

                        selecting = "target_file"
                        time.sleep(3)
                        break  # Exit loop and continue

                    gesture = gesture_recognizer.get_gesture()  # Wait for new valid gesture

            elif selecting == "target_file":
                if gesture in gesture_recognizer.gesture_to_file:
                    target_file = gesture_recognizer.gesture_to_file[gesture]
                    print(f"Locked Destination Column: {chr(ord('A') + target_file)}")
                    selecting = "target_rank"

                    # Highlight destination column in red
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0, 100),  # Red column highlight
                        pygame.Rect(target_file * SQUARE_SIZE, 0, SQUARE_SIZE, SCREEN_SIZE),
                        0
                    )
                    pygame.display.flip()
                    time.sleep(3)

            elif selecting == "target_rank":
                if gesture in gesture_recognizer.gesture_to_rank:
                    target_rank = gesture_recognizer.gesture_to_rank[gesture]
                    print(f"Locked Destination Row: {target_rank + 1}")

                    # Highlight destination square with red border
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),  # Red outline
                        pygame.Rect(target_file * SQUARE_SIZE, (7 - target_rank) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        5
                    )
                    pygame.display.flip()
                    time.sleep(3)

                    # Move the piece if it's a legal move
                    start_square = chess.square(selected_file, selected_rank)
                    end_square = chess.square(target_file, target_rank)
                    move = chess.Move(from_square=start_square, to_square=end_square)

                    if move in engine.board.legal_moves:
                        engine.make_move(move.uci())

                        if engine.is_game_over():
                            print("Game Over!")
                            return

                    else:
                        print("Invalid move: This is not a legal move.")
                        time.sleep(2)

                    # Reset selections for next turn
                    selected_file = None
                    selected_rank = None
                    target_file = None
                    target_rank = None
                    selecting = "file"

        # Draw evaluation bar
        evaluation = evaluate_board(engine)
        evaluation_bar.draw(evaluation)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
