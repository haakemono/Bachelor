import os
from PIL import Image, ImageTk
from Constants import ASSETS_PATH, SQUARE_SIZE, SCREEN_SIZE, BAR_WIDTH, STOCKFISH_PATH
import pygame
from engine import ChessEngine
from chessboard import ChessBoard
from evaluation_bar import EvaluationBar
from hand_tracking import HandTracker


def load_piece_images(directory):
    """
    Load piece images from the assets directory.
    """
    pieces = {
        'r': 'br', 'n': 'bn', 'b': 'bb', 'q': 'bq', 'k': 'bk', 'p': 'bp',  # Black pieces
        'R': 'wr', 'N': 'wn', 'B': 'wb', 'Q': 'wq', 'K': 'wk', 'P': 'wp'   # White pieces
    }
    images = {}
    for piece, filename in pieces.items():
        file_path = os.path.join(directory, f"{filename}.png")
        if os.path.exists(file_path):
            images[piece] = ImageTk.PhotoImage(Image.open(file_path).resize((50, 50)))
        else:
            print(f"Missing image for piece: {filename}")
    return images


def handle_game_over(screen, engine):
    """Display the game over message and stop processing moves."""
    font = pygame.font.Font(None, 74)
    result = engine.get_game_result()
    if result == "1-0":
        message = "White wins!"
    elif result == "0-1":
        message = "Black wins!"
    else:
        message = "Stalemate!"

    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()


def initialize_game():
    """Initialize pygame, screen, engine, and components."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE + BAR_WIDTH + 100, SCREEN_SIZE))
    pygame.display.set_caption("Chess")
    engine = ChessEngine(STOCKFISH_PATH)
    chessboard = ChessBoard(engine, ASSETS_PATH, SQUARE_SIZE)
    evaluation_bar = EvaluationBar(screen, SCREEN_SIZE, SCREEN_SIZE, BAR_WIDTH)
    hand_tracker = HandTracker(width=SCREEN_SIZE)
    return screen, engine, chessboard, evaluation_bar, hand_tracker
