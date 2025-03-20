import pygame
import chess
import os
import time
from chessboard import ChessBoard
from engine import ChessEngine
from gesture_recognition import GestureRecognizer

BASE_PATH = os.path.dirname(__file__)
ASSETS_PATH = os.path.join(BASE_PATH, "assets")
SQUARE_SIZE = 80
SCREEN_SIZE = SQUARE_SIZE * 8
BAR_WIDTH = 20

# -----------------------------------------
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

# -----------------------------------------
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
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    skill_level = max(1, skill_level - 1)
                elif event.key == pygame.K_RIGHT:
                    skill_level = min(10, skill_level + 1)
                elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                    control_mode_index = (control_mode_index + 1) % len(control_modes)
                elif event.key == pygame.K_RETURN:
                    return skill_level, control_modes[control_mode_index]

# -----------------------------------------
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

# -----------------------------------------
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

# -----------------------------------------
def handle_gesture_input(gesture, selecting, engine, gesture_recognizer, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank):
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
                engine.make_move(move.uci())
                print(f"Player move: {move.uci()}")
                return "file", None, None, None, [], None, None  # Reset
            else:
                print("Invalid move")
                selecting = "file"
    return selecting, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank

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
                    main()  # Restart the game
                    return

# -----------------------------------------
def main():
    skill_level, control_mode = start_menu()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH, SCREEN_SIZE + 30))
    pygame.display.set_caption("Chess")

    try:
        stockfish_path = r"C:\\Users\\haako\\OneDrive\\Documents\\Skole\\stockfish-windows-x86-64-avx2\\stockfish\\stockfish-windows-x86-64-avx2.exe"
        if not os.path.exists(stockfish_path): raise FileNotFoundError()
    except:
        stockfish_path = "/opt/homebrew/bin/stockfish"
        if not os.path.exists(stockfish_path): raise FileNotFoundError("Install Stockfish first.")

    engine = ChessEngine(stockfish_path)
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    gesture_recognizer = GestureRecognizer()

    selecting = "file"
    selected_piece_square = None
    selected_file = selected_rank = target_file = target_rank = None
    valid_moves = []
    clock = pygame.time.Clock()

    while True:
        screen.fill((0, 0, 0))
        chessboard.draw(screen)
        events = pygame.event.get()

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                engine.close()
                gesture_recognizer.print_average_confidences()
                return

        for move in valid_moves:
            pygame.draw.circle(screen, (255, 0, 0), (move[0] * SQUARE_SIZE + SQUARE_SIZE // 2, (7 - move[1]) * SQUARE_SIZE + SQUARE_SIZE // 2), 10)

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
                            engine.make_move(move.uci())
                            engine.turn = "black"
                        selecting = "file"
                        selected_piece_square = None
                        valid_moves = []

                if engine.is_game_over():
                    result = engine.get_game_result()
                    gesture_recognizer.print_average_confidences()
                    show_game_over_screen(result)
                    return

            elif input_result[0] == "gesture":
                selecting, selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank = handle_gesture_input(
                    input_result[1], selecting, engine, gesture_recognizer,
                    selected_file, selected_rank, selected_piece_square, valid_moves, target_file, target_rank)
                if selecting == "file":
                    engine.turn = "black"

                if engine.is_game_over():
                    result = engine.get_game_result()
                    gesture_recognizer.print_average_confidences()
                    show_game_over_screen(result)
                    return

        if engine.turn == "black":
            print("AI is thinking...")
            ai_move = engine.ai_move(skill_level=skill_level)
            print(f"AI move: {ai_move}")
            engine.turn = "white"

            if engine.is_game_over():
                result = engine.get_game_result()
                gesture_recognizer.print_average_confidences()
                show_game_over_screen(result)
                return



        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
