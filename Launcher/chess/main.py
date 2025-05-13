import pygame
import chess
import os
from chessboard import ChessBoard
from engine import ChessEngine
import gesture_recognition as gesture_recognizer

"""
Constants for board setup and screen size
"""
BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
SQUARE_SIZE = 90
SCREEN_SIZE = SQUARE_SIZE * 8
BAR_WIDTH = 20

"""
Evaluates the current board state based on piece values (basic heuristic)
"""
def evaluate_board(engine):
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

"""
Displays a simple start menu where user selects AI skill level and control mode
"""
def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Chess Game - Start Menu")
    font = pygame.font.SysFont(None, 36)
    skill_level = 5
    control_modes = ["gesture", "mouse"]
    control_mode_index = 0

    while True:
        screen.fill((30, 30, 30))
        screen.blit(font.render("Select AI Skill Level (1-10)", True, (255, 255, 255)), (150, 50))
        screen.blit(font.render(f"Skill Level: {skill_level}", True, (255, 255, 0)), (220, 100))
        screen.blit(font.render(f"Control Mode: {control_modes[control_mode_index]}", True, (0, 200, 255)), (170, 160))
        screen.blit(font.render("←/→ : Change Skill Level", True, (180, 180, 180)), (140, 240))
        screen.blit(font.render("↑/↓ : Toggle Control Mode", True, (180, 180, 180)), (140, 270))
        screen.blit(font.render("Enter : Start Game", True, (180, 180, 180)), (140, 300))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    skill_level = max(1, skill_level - 1)
                elif event.key == pygame.K_RIGHT:
                    skill_level = min(10, skill_level + 1)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    control_mode_index = (control_mode_index + 1) % len(control_modes)
                elif event.key == pygame.K_RETURN:
                    return skill_level, control_modes[control_mode_index]
"""
Gets user input via gesture or mouse depending on selected control mode
"""
def get_player_input(events, control_mode, gesture_recognizer=None):
    if control_mode == "gesture":
        gesture = gesture_recognizer.get_move_gesture()
        return ("gesture", gesture) if gesture else None
    elif control_mode == "mouse":
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < SCREEN_SIZE and y < SCREEN_SIZE:
                    file = x // SQUARE_SIZE
                    rank = 7 - (y // SQUARE_SIZE)
                    return ("mouse", file, rank)
    return None

"""
Handles piece selection and movement using mouse input
Returns updated selection state and move info
"""
def handle_mouse_input(input_result, selecting, engine, selected_piece_square, valid_moves):
    if selecting == "file":
        selected_file, selected_rank = input_result[1], input_result[2]
        square = chess.square(selected_file, selected_rank)
        piece = engine.board.piece_at(square)
        if piece is None or piece.color != engine.board.turn:
            return selecting, None, None, None, []
        valid_moves = [(chess.square_file(m), chess.square_rank(m)) for m in engine.get_valid_moves(square)]
        return "target", square, selected_file, selected_rank, valid_moves
    elif selecting == "target":
        target_file, target_rank = input_result[1], input_result[2]
        return "move", (target_file, target_rank), None, None, []
    return selecting, None, None, None, valid_moves

"""
Handles piece selection and movement using gestures
Converts gestures to board coordinates and builds a move
"""
def handle_gesture_input(gesture, selecting, engine, gesture_recognizer,
                         selected_file, selected_rank, selected_piece_square,
                         valid_moves, target_file, target_rank):
    if selecting == "file":
        if gesture in gesture_recognizer.gesture_to_file:
            selected_file = gesture_recognizer.gesture_to_file[gesture]
            print(f"Selected file (column): {selected_file}")
            selecting = "rank"

    elif selecting == "rank":
        if gesture in gesture_recognizer.gesture_to_rank:
            selected_rank = gesture_recognizer.gesture_to_rank[gesture]
            print(f"Selected rank (row): {selected_rank}")
            square = chess.square(selected_file, selected_rank)
            piece = engine.board.piece_at(square)
            if piece is None or piece.color != engine.board.turn:
                selecting = "file"
            else:
                selected_piece_square = square
                valid_moves = [(chess.square_file(m), chess.square_rank(m)) for m in engine.get_valid_moves(square)]
                selecting = "target_file"

    elif selecting == "target_file":
        if gesture in gesture_recognizer.gesture_to_file:
            target_file = gesture_recognizer.gesture_to_file[gesture]
            print(f"Target file (column): {target_file}")
            selecting = "target_rank"

    elif selecting == "target_rank":
        if gesture in gesture_recognizer.gesture_to_rank:
            target_rank = gesture_recognizer.gesture_to_rank[gesture]
            print(f"Target rank (row): {target_rank}")
            end_square = chess.square(target_file, target_rank)
            move = chess.Move(selected_piece_square, end_square)
            if move in engine.board.legal_moves:
                return "animate", selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank, move
            else:
                print("Invalid move")
                selecting = "file"

    return selecting, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank
"""
Displays the game over screen and waits for user to restart or quit
"""
def show_game_over_screen(result):
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Game Over")
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    while True:
        screen.fill((20, 20, 20))
        screen.blit(font.render("Game Over", True, (255, 0, 0)), (200, 80))
        screen.blit(small_font.render(f"Result: {result}", True, (255, 255, 255)), (200, 150))
        screen.blit(small_font.render("Press R to Restart", True, (180, 180, 180)), (180, 230))
        screen.blit(small_font.render("Press Q to Quit", True, (180, 180, 180)), (200, 270))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_r:
                    main()
                    return
"""#
The main function sets up the chess game, handles user input, draws the board, runs AI moves, 
and keeps the game loop running until the player quits or restarts.
"""
def main():
    skill_level, control_mode = start_menu()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH + 200, SCREEN_SIZE + 30))  # Wider screen for sidebar
    pygame.display.set_caption("Chess")

    # UNIVERSAL STOCKFISH PATH HANDLING
    base_path = os.path.dirname(os.path.abspath(__file__))
    stockfish_folder = os.path.join(base_path, "stockfish")
    possible_names = ["stockfish", "stockfish.exe"]

    stockfish_path = next(
        (os.path.join(stockfish_folder, name) for name in possible_names
         if os.path.exists(os.path.join(stockfish_folder, name))),
        None
    )

    if not stockfish_path:
        raise FileNotFoundError(
            "Stockfish binary not found.\n"
            "Download it from https://stockfishchess.org/download/ and place it in:\n"
            f"{stockfish_folder}"
        )

    # Initialize engine with the detected path
    engine = ChessEngine(stockfish_path)
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)

    

    selecting = "file"
    selected_piece_square = None
    selected_file = selected_rank = target_file = target_rank = None
    valid_moves = []
    move_log = []
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)

    while True:
        screen.fill((0, 0, 0))
        chessboard.draw(screen)

        # Draw highlight squares
        if selected_piece_square is not None:
            r = 7 - chess.square_rank(selected_piece_square)
            c = chess.square_file(selected_piece_square)
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill((50, 50, 255, 100))
            screen.blit(s, (c * SQUARE_SIZE, r * SQUARE_SIZE))

            for move in valid_moves:
                mf, mr = move
                pygame.draw.circle(screen, (255, 255, 0), (mf * SQUARE_SIZE + SQUARE_SIZE // 2, (7 - mr) * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

        # Draw move log sidebar
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(SCREEN_SIZE + BAR_WIDTH, 0, 200, SCREEN_SIZE + 30))
        max_display_lines = (SCREEN_SIZE + 30 - 20) // 20
        start_index = max(0, len(move_log) - 2 * max_display_lines)
        for i in range(start_index, len(move_log), 2):
            move_text = f"{i // 2 + 1}. {move_log[i]}"
            if i + 1 < len(move_log):
                move_text += f" {move_log[i + 1]}"
            text_surface = font.render(move_text, True, (255, 255, 255))
            screen.blit(text_surface, (SCREEN_SIZE + BAR_WIDTH + 10, 10 + (i - start_index) * 10))

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                engine.close()
                gesture_recognizer.print_average_confidences()
                return

        input_result = get_player_input(events, control_mode, gesture_recognizer)

        if engine.turn == "white" and input_result:
            if input_result[0] == "mouse":
                if selecting == "file":
                    selecting, selected_piece_square, selected_file, selected_rank, valid_moves = handle_mouse_input(
                        input_result, selecting, engine, selected_piece_square, valid_moves)
                elif selecting == "target":
                    selecting, target_pos, _, _, _ = handle_mouse_input(input_result, selecting, engine, selected_piece_square, valid_moves)
                    if target_pos:
                        target_file, target_rank = target_pos
                        end_square = chess.square(target_file, target_rank)
                        move = chess.Move(selected_piece_square, end_square)
                        if move in engine.board.legal_moves:
                            chessboard.animate_move(screen, selected_piece_square, end_square)
                            move_log.append(move.uci())
                            engine.make_move(move.uci())
                            engine.turn = "black"
                        selecting = "file"
                        selected_piece_square = None
                        valid_moves = []

            elif input_result[0] == "gesture":
                result = handle_gesture_input(
                    input_result[1], selecting, engine, gesture_recognizer,
                    selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank
                )

                if result[0] == "animate":
                    _, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank, move = result
                    piece = engine.get_piece_at(move.from_square)
                    if piece:
                        piece_image = chessboard.get_piece_image(piece)
                        chessboard.animate_move(screen, move.from_square, move.to_square, piece_image)
                    engine.make_move(move.uci())
                    move_log.append(move.uci())
                    engine.turn = "black"
                    selecting = "file"
                    selected_piece_square = None
                    valid_moves = []
                else:
                    selecting, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank = result

        if engine.is_game_over():
            result = engine.get_game_result()

            screen.fill((0, 0, 0))
            chessboard.draw(screen)

            font_big = pygame.font.SysFont("Arial", 48)
            font_small = pygame.font.SysFont("Arial", 28)

            screen.blit(font_big.render("Game Over", True, (255, 0, 0)), (SCREEN_SIZE // 2 - 120, SCREEN_SIZE // 2 - 60))
            screen.blit(font_small.render(f"Result: {result}", True, (255, 255, 255)), (SCREEN_SIZE // 2 - 80, SCREEN_SIZE // 2))

            if control_mode == "gesture":
                avg_confidences = gesture_recognizer.get_average_confidences()
                screen.blit(font_small.render("Gesture Accuracy (%)", True, (255, 255, 0)), (SCREEN_SIZE + BAR_WIDTH + 10, 40))

                y_offset = 70
                for gesture, avg in avg_confidences.items():
                    display_text = f"{gesture}: {avg:.1f}%"
                    screen.blit(font_small.render(display_text, True, (255, 255, 255)), (SCREEN_SIZE + BAR_WIDTH + 10, y_offset))
                    y_offset += 30
            else:
                screen.blit(font_small.render("Move Log", True, (255, 255, 0)), (SCREEN_SIZE + BAR_WIDTH + 10, 40))

                y_offset = 70
                start_index = max(0, len(move_log) - 2 * 20)  # Show last ~20 lines
                for i in range(start_index, len(move_log), 2):
                    move_text = f"{i // 2 + 1}. {move_log[i]}"
                    if i + 1 < len(move_log):
                        move_text += f" {move_log[i + 1]}"
                    text_surface = font_small.render(move_text, True, (255, 255, 255))
                    screen.blit(text_surface, (SCREEN_SIZE + BAR_WIDTH + 10, y_offset))
                    y_offset += 30

            screen.blit(font_small.render("Press R to Restart or Q to Quit", True, (180, 180, 180)), (SCREEN_SIZE // 2 - 150, SCREEN_SIZE + 10))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pygame.quit(); exit()
                        elif event.key == pygame.K_r:
                            main()
                            return

        if engine.turn == "black":
            print("AI is thinking...")
            ai_move = engine.ai_move(skill_level=skill_level)
            chessboard.animate_move(screen, ai_move.from_square, ai_move.to_square)
            move_log.append(ai_move.uci())
            engine.board.push(ai_move)
            engine.turn = "white"

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
