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



##HOVERING MAIN
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE))
    pygame.display.set_caption("Chess")

    # Initialize chess engine, chessboard, evaluation bar, and hand tracker
    engine = ChessEngine()
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    hand_tracker = HandTracker(width=SCREEN_SIZE)

    hover_start_time = None  # Track when hovering started
    hovered_square = None  # Current square being hovered over
    selected_square = None  # Square with selected piece
    valid_moves = []  # Valid moves for the selected piece
    running = True
    game_over = False

    clock = pygame.time.Clock()
    frame_count = 0  # Counter to track frames
    
    # Initialize smoothed positions "HERE"
    smoothed_x, smoothed_y = SCREEN_SIZE // 2, SCREEN_SIZE // 2  # Start in the center of the board
    alpha = 0.9  # Smoothing factor (higher = less smoothing)


    while running:
        frame_count += 1

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the hand position
        player_position = hand_tracker.get_player_position()
        if player_position:
            dot_x, dot_y = player_position
            print(f"Drawing dot at: {dot_x}, {dot_y}")  # Debugging line
            
            # Apply smoothing "HERE"
            smoothed_x = int(alpha * dot_x + (1 - alpha) * smoothed_x)
            smoothed_y = int(alpha * dot_y + (1 - alpha) * smoothed_y)
            print(f"Smoothed position: ({smoothed_x}, {smoothed_y})")  # Debugging
            
            # Chessboard edges for debugging
            x_min, x_max = 0, SCREEN_SIZE - SQUARE_SIZE
            y_min, y_max = 0, SCREEN_SIZE - SQUARE_SIZE
            print(f"Chessboard edges: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")  # Debugging


            # Ensure the dot stays within the chessboard boundaries
            smoothed_x = max(x_min, min(x_max, smoothed_x))  # Ensure x stays within bounds
            smoothed_y = max(y_min, min(y_max, smoothed_y))  # Ensure y stays within bounds
            
            
#            # Ensure dot stays within the board boundaries
#            dot_x = max(0, min(SCREEN_SIZE - 1, dot_x))
#            dot_y = max(0, min(SCREEN_SIZE - 1, dot_y))

            # Map dot position to chessboard squares
            # Map dot position to chessboard squares
            col = min(max(dot_x // SQUARE_SIZE, 0), 7)  # Ensure col is in range 0-7
            row = min(max(dot_y // SQUARE_SIZE, 0), 7)  # Ensure row is in range 0-7



            # Convert dot position to board square
            square = chess.square(col, 7 - row)


            
            # Hovering logic
            if hovered_square == square:
                # If the dot stays on the same square, track hover time
                if hover_start_time is None:
                    hover_start_time = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - hover_start_time >= 2000:  # 2 seconds hover
                    print(f"Clicking on square: {square}")  # Debugging line

                    if selected_square is None:
                        # Select the piece on the square if it's valid
                        piece = engine.board.piece_at(square)
                        if piece and ((piece.color and engine.turn == "white") or (not piece.color and engine.turn == "black")):
                            selected_square = square
                            valid_moves = [move.to_square for move in engine.board.legal_moves if move.from_square == square]
                            print(f"Piece selected: {piece}, Valid moves: {valid_moves}")  # Debugging line
                    else:
                        # Attempt to move the selected piece
                        if square in valid_moves:
                            move = chess.Move(from_square=selected_square, to_square=square)
                            if engine.make_move(move.uci()):
                                if engine.is_game_over():
                                    game_over = True
                                    print("Game Over:", engine.get_game_result())
                        # Reset selection after the move
                        selected_square = None
                        valid_moves = []
                    hover_start_time = None  # Reset hover timer after "click"
            else:
                # Reset hover timer if the dot moves to a new square
                hovered_square = square
                hover_start_time = pygame.time.get_ticks()

        # Redraw the chessboard every 2nd frame
        if frame_count % 2 == 0:
            screen.fill((0, 0, 0))  # Clear the screen
            chessboard.draw(screen)

            # Highlight selected square and valid moves
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



        # Always draw the dot
        if player_position:
            pygame.draw.circle(screen, (255, 0, 0), (dot_x, dot_y), 15)

        # Display game-over message
        if game_over:
            font = pygame.font.Font(None, 74)
            result = engine.get_game_result()
            message = "Checkmate!" if result in ["1-0", "0-1"] else "Stalemate!"
            text = font.render(message, True, (255, 0, 0))
            text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
            screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    # Clean up
    hand_tracker.release()
    pygame.quit()







if __name__ == "__main__":
    main()

