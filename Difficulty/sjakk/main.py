import pygame
import chess
from chessboard import ChessBoard
from engine import ChessEngine
from evaluation_bar import EvaluationBar
from handtracking import HandTracker
# Constants
ASSETS_PATH = "assets"
SQUARE_SIZE = 80
SCREEN_SIZE = SQUARE_SIZE * 8
BAR_WIDTH = 20
HOVER_TIME_TRESHOLD = 3

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
        chess.KING: 0  # King value isn't needed for evaluation
    }

    evaluation = 0
    for square in chess.SQUARES:
        piece = engine.board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            evaluation += value if piece.color else -value
    return evaluation

def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE))
    pygame.display.set_caption("Chess")

    # Initialize chess engine
    engine = ChessEngine()

    # Initialize chessboard, evaluation bar, and hand tracker (ADDED)
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)
    hand_tracker = HandTracker(width=SCREEN_SIZE)  # ADDED

    # Variables for hovering logic (ADDED)
    hover_start_time = None
    hovered_square = None
    selected_square = None
    valid_moves = []
    running = True
    game_over = False
    
    # Variables for smoothing (ADDED)
    smoothed_x, smoothed_y = SCREEN_SIZE // 2, SCREEN_SIZE // 2  # Start in the center
    #----------------------------------------------SENSITIVITET PÅ KAMERAET----------------------------------------------------#
    alpha = 0.9  # Smoothing factor (higher = less smoothing)

    clock = pygame.time.Clock()
    frame_count = 0  # Frame counter for optimizations

    while running:
        frame_count += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the hand position (ADDED)
        player_position = hand_tracker.get_player_position()
        if player_position:
            dot_x, dot_y = player_position
            smoothed_x = int(alpha * dot_x + (1 - alpha) * smoothed_x)  # ADDED: Smoothing
            smoothed_y = int(alpha * dot_y + (1 - alpha) * smoothed_y)

            # Ensure dot stays within the chessboard boundaries (ADDED)
            x_min, x_max = 0, SCREEN_SIZE - 1
            y_min, y_max = 0, SCREEN_SIZE - 1
            smoothed_x = max(x_min, min(x_max, smoothed_x))
            smoothed_y = max(y_min, min(y_max, smoothed_y))

            # Map smoothed dot position to chessboard square (ADDED)
            col = smoothed_x // SQUARE_SIZE
            row = smoothed_y // SQUARE_SIZE
            square = chess.square(col, 7 - row)

            # Hovering logic (ADDED)
            if hovered_square == square:
                if hover_start_time is None:
                    hover_start_time = pygame.time.get_ticks()  # Start hovering timer
                elif pygame.time.get_ticks() - hover_start_time >= 2000:  # Hover for 2 seconds
                    if selected_square is None:
                        # Select the piece
                        piece = engine.board.piece_at(square)
                        if piece and ((piece.color and engine.turn == "white") or (not piece.color and engine.turn == "black")):
                            selected_square = square
                            valid_moves = [move.to_square for move in engine.board.legal_moves if move.from_square == square]
                    else:
                        # Make the move
                        if square in valid_moves:
                            move = chess.Move(from_square=selected_square, to_square=square)
                            if engine.make_move(move.uci()):
                                if engine.is_game_over():
                                    game_over = True
                        selected_square = None
                        valid_moves = []
                    hover_start_time = None  # Reset hover timer
            else:
                hovered_square = square
                hover_start_time = pygame.time.get_ticks()


        # Redraw chessboard every second frame (MODIFIED: Optimization)
        if frame_count % 2 == 0:
            screen.fill((0, 0, 0))  # Clear the screen
            chessboard.draw(screen)

        # Highlight selected square and valid moves (MODIFIED)
        if selected_square is not None:
            selected_row, selected_col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
            pygame.draw.rect(
                screen,
                (255, 255, 0, 100),
                pygame.Rect(selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                5,
            )
            for move in valid_moves:
                move_row, move_col = 7 - chess.square_rank(move), chess.square_file(move)
                pygame.draw.circle(
                    screen,
                    (0, 255, 0, 150),
                    (move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    10,
                )

            # Draw the dot representing hand position (ADDED)
        if player_position:
            pygame.draw.circle(screen, (255, 0, 0), (smoothed_x, smoothed_y), 15)
        # Draw the evaluation bar
        evaluation = evaluate_board(engine)
        evaluation_bar.draw(evaluation)

        # Display game-over message
        if game_over:
            font = pygame.font.Font(None, 74)
            result = engine.get_game_result()
            message = "Checkmate!" if result in ["1-0", "0-1"] else "Stalemate!"
            text = font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            screen.blit(text, text_rect)

        # Update display
        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    main()
