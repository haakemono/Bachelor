import pygame
import chess
from chessboard import ChessBoard
from engine import ChessEngine
from evaluation_bar import EvaluationBar

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

    # Initialize chessboard and evaluation bar
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)

    selected_square = None
    valid_moves = []
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                print(f"Mouse clicked at: ({mouse_x}, {mouse_y})")  # Debugging

                if mouse_x < SCREEN_SIZE:  # Ignore clicks in the evaluation bar
                    col = mouse_x // SQUARE_SIZE
                    row = mouse_y // SQUARE_SIZE
                    square = chess.square(col, 7 - row)
                    print(f"Clicked square: {square}, Row: {row}, Col: {col}")  # Debugging

                    if selected_square is None:
                        # Select a piece
                        piece = engine.board.piece_at(square)
                        print(f"Piece at clicked square: {piece}")  # Debugging
                        if piece and ((piece.color and engine.turn == "white") or (not piece.color and engine.turn == "black")):
                            selected_square = square
                            valid_moves = [move.to_square for move in engine.board.legal_moves if move.from_square == square]
                            print(f"Selected piece: {piece}, Valid moves: {valid_moves}")  # Debugging
                    else:
                        # Attempt to make a move
                        if square in valid_moves:
                            move = chess.Move(from_square=selected_square, to_square=square)
                            if engine.make_move(move.uci()):
                                print(f"Move {move.uci()} executed")
                                if engine.is_game_over():
                                    game_over = True
                                    print("Game Over:", engine.get_game_result())
                        # Reset selection
                        selected_square = None
                        valid_moves = []

        # Draw the chessboard
        chessboard.draw(screen)

        # Highlight selected square and valid moves
        if selected_square is not None:
            # Highlight the selected square
            selected_row, selected_col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
            pygame.draw.rect(
                screen,
                (255, 255, 0, 100),
                pygame.Rect(selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                5,
            )

            # Highlight valid moves
            for move in valid_moves:
                move_row, move_col = 7 - chess.square_rank(move), chess.square_file(move)
                pygame.draw.circle(
                    screen,
                    (0, 255, 0, 150),
                    (move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    10,
                )

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
