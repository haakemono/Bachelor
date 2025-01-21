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

def draw_promotion_menu(screen, color, square_size):
    """
    Draws the promotion menu for selecting a piece.

    Args:
        screen (pygame.Surface): The game screen.
        color (str): 'w' for white, 'b' for black.
        square_size (int): Size of a chess square.

    Returns:
        dict: A dictionary mapping piece type to rect for click detection.
    """
    pieces = ['q', 'r', 'b', 'n']  # Queen, Rook, Bishop, Knight
    piece_rects = {}
    menu_width = len(pieces) * square_size
    menu_x = (SCREEN_SIZE - menu_width) // 2
    menu_y = (SCREEN_SIZE - square_size) // 2

    # Draw each piece option
    for i, piece in enumerate(pieces):
        piece_image = pygame.image.load(f"{ASSETS_PATH}/{color}{piece}.png")
        piece_image = pygame.transform.scale(piece_image, (square_size, square_size))
        rect = pygame.Rect(menu_x + i * square_size, menu_y, square_size, square_size)
        screen.blit(piece_image, rect.topleft)
        piece_rects[piece] = rect

    pygame.display.flip()
    return piece_rects

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE))
    pygame.display.set_caption("Chess")

    engine = ChessEngine()
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)

    selected_square = None
    valid_moves = []
    running = True
    game_over = False
    promotion_menu = None
    move = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if promotion_menu:
                    # Handle promotion menu selection
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        for piece, rect in promotion_menu.items():
                            if rect.collidepoint(mouse_x, mouse_y):
                                promotion_map = {'q': chess.QUEEN, 'r': chess.ROOK, 'b': chess.BISHOP, 'n': chess.KNIGHT}
                                move.promotion = promotion_map[piece]
                                if engine.make_move(move.uci()):
                                    print(f"Move {move.uci()} executed with promotion to {piece.upper()}")
                                    # Check for threefold repetition
                                    if engine.board.is_repetition(3):
                                        print("Threefold repetition detected. The game is a draw.")
                                        game_over = True
                                promotion_menu = None
                                selected_square = None
                                valid_moves = []
                                break
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if mouse_x < SCREEN_SIZE:
                            col = mouse_x // SQUARE_SIZE
                            row = mouse_y // SQUARE_SIZE
                            square = chess.square(col, 7 - row)

                            piece = engine.board.piece_at(square)
                            if piece and ((piece.color and engine.turn == "white") or (not piece.color and engine.turn == "black")):
                                selected_square = square
                                valid_moves = [move.to_square for move in engine.board.legal_moves if move.from_square == square]
                            elif square in valid_moves:
                                move = chess.Move(from_square=selected_square, to_square=square)

                                if engine.board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
                                    promotion_menu = draw_promotion_menu(screen, 'w' if engine.board.turn else 'b', SQUARE_SIZE)
                                else:
                                    if engine.make_move(move.uci()):
                                        print(f"Move {move.uci()} executed")
                                        # Check for threefold repetition
                                        if engine.board.is_repetition(3):
                                            print("Threefold repetition detected. The game is a draw.")
                                            game_over = True

                                        if engine.is_game_over():
                                            game_over = True
                                            print("Game Over:", engine.get_game_result())

                                selected_square = None
                                valid_moves = []
                            else:
                                selected_square = None
                                valid_moves = []

        # Draw the chessboard
        if not promotion_menu:
            chessboard.draw(screen)

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

            evaluation = evaluate_board(engine)
            evaluation_bar.draw(evaluation)

            if game_over:
                font = pygame.font.Font(None, 74)
                message = "Draw by repetition" if engine.board.is_repetition(3) else "Game Over"
                text = font.render(message, True, (255, 0, 0))
                text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
                screen.blit(text, text_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
