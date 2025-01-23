import pygame
import chess
from chessboard import ChessBoard
from engine import ChessEngine
from evaluation_bar import EvaluationBar
from hand_tracking import HandTracker

# Constants
ASSETS_PATH = "assets"
SQUARE_SIZE = 80
SCREEN_SIZE = SQUARE_SIZE * 8
BAR_WIDTH = 20
HOVER_TIME_THRESHOLD = 3  # Seconds

def evaluate_board(engine):
    """
    A basic evaluation function that calculates the material balance.
    Positive for white, negative for black.
    """
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
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
    stockfish_path = r"C:\\Users\\haako\\Downloads\\stockfish-windows-x86-64\\stockfish\\stockfish-windows-x86-64.exe"
    engine = ChessEngine(stockfish_path)

    # Initialize chessboard, evaluation bar, and hand tracker
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)
    hand_tracker = HandTracker(width=SCREEN_SIZE)

    hover_start_time = None
    hovered_square = None
    selected_square = None
    valid_moves = []
    bot_last_move = None  # Track bot's last move
    running = True
    game_over = False
    player_turn = True  # True = human's turn, False = bot's turn

    smoothed_x, smoothed_y = SCREEN_SIZE // 2, SCREEN_SIZE // 2
    alpha = 0.9

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # If the game is over, display the result and stop processing moves
        if game_over:
            font = pygame.font.Font(None, 74)
            result = engine.get_game_result()
            if result == "1-0":
                message = "White wins!"  # Player wins
            elif result == "0-1":
                message = "Black wins!"  # Bot wins
            else:
                message = "Stalemate!"

            # Display the result message on the screen
            text = font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            continue

        if player_turn:
            # Get the hand position
            player_position = hand_tracker.get_player_position()
            if player_position:
                dot_x, dot_y = player_position
                smoothed_x = int(alpha * dot_x + (1 - alpha) * smoothed_x)
                smoothed_y = int(alpha * dot_y + (1 - alpha) * smoothed_y)

                # Ensure the dot stays within the chessboard boundaries
                smoothed_x = max(0, min(SCREEN_SIZE - 1, smoothed_x))
                smoothed_y = max(0, min(SCREEN_SIZE - 1, smoothed_y))

                # Map smoothed dot position to chessboard square
                col = smoothed_x // SQUARE_SIZE
                row = smoothed_y // SQUARE_SIZE
                square = chess.square(col, 7 - row)

                # Hovering logic
                if hovered_square == square:
                    if hover_start_time is None:
                        hover_start_time = pygame.time.get_ticks()
                    elif pygame.time.get_ticks() - hover_start_time >= 2000:
                        if selected_square is None:
                            piece = engine.board.piece_at(square)
                            if piece and piece.color == chess.WHITE:  # Only allow white moves
                                selected_square = square
                                valid_moves = [move.to_square for move in engine.board.legal_moves if move.from_square == square]
                        else:
                            if square in valid_moves:
                                move = chess.Move(from_square=selected_square, to_square=square)
                                if engine.make_move(move.uci()):
                                    if engine.is_game_over():
                                        game_over = True
                                    player_turn = False  # Switch to bot's turn
                                    selected_square = None
                                    valid_moves = []
                        hover_start_time = None
                else:
                    hovered_square = square
                    hover_start_time = pygame.time.get_ticks()
        else:
            # Bot's turn
            move = engine.get_best_move()  # Get the best move from Stockfish
            if move:
                bot_last_move = move  # Track the bot's last move
                engine.make_move(move.uci())
                player_turn = True  # Switch back to player's turn
                if engine.is_game_over():
                    game_over = True

        # Draw the chessboard
        screen.fill((0, 0, 0))  # Clear the screen
        chessboard.draw(screen)

        # Highlight selected square and valid moves
        if selected_square is not None:
            selected_row, selected_col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
            pygame.draw.rect(
                screen,
                (255, 255, 0),
                pygame.Rect(selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                5,
            )
            for move in valid_moves:
                move_row, move_col = 7 - chess.square_rank(move), chess.square_file(move)
                pygame.draw.circle(
                    screen,
                    (0, 255, 0),
                    (move_col * SQUARE_SIZE + SQUARE_SIZE // 2, move_row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    10,
                )

        # Highlight the bot's last move
        if bot_last_move:
            from_square, to_square = bot_last_move.from_square, bot_last_move.to_square
            from_row, from_col = 7 - chess.square_rank(from_square), chess.square_file(from_square)
            to_row, to_col = 7 - chess.square_rank(to_square), chess.square_file(to_square)

            # Highlight the "from" square in blue
            pygame.draw.rect(
                screen, (0, 0, 255),
                pygame.Rect(from_col * SQUARE_SIZE, from_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5
            )
            # Highlight the "to" square in blue
            pygame.draw.rect(
                screen, (0, 0, 255),
                pygame.Rect(to_col * SQUARE_SIZE, to_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5
            )

        # Always draw the dot
        if player_position:
            pygame.draw.circle(screen, (255, 0, 0), (smoothed_x, smoothed_y), 15)

        # Draw the evaluation bar
        evaluation = evaluate_board(engine)
        evaluation_bar.draw(evaluation)

        # Update display
        pygame.display.flip()
        clock.tick(30)

    # Clean up
    hand_tracker.release()
    pygame.quit()

if __name__ == "__main__":
    main()
