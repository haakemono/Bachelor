import pygame as p
import chess
import chess.engine
import os

# Constants
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
MAX_FPS = 15

# Path to Stockfish executable (update this path to where you downloaded Stockfish)
stockfish_path = r"C:\Users\haako\OneDrive\Documents\Skole\stockfish-windows-x86-64-avx2\stockfish.exe"

# Initialize Pygame
p.init()
screen = p.display.set_mode((BOARD_SIZE, BOARD_SIZE))
clock = p.time.Clock()

def draw_board(screen, board):
    """Draw the chess board and pieces."""
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board.piece_at(r * 8 + c)
            if piece:
                font = p.font.Font(None, 32)
                piece_name = piece.symbol()
                text = font.render(piece_name, True, p.Color('black'))
                screen.blit(text, (c * SQUARE_SIZE + SQUARE_SIZE // 4, r * SQUARE_SIZE + SQUARE_SIZE // 4))

def play_vs_ai():
    """The game loop where the player plays against the AI."""
    board = chess.Board()

    while not board.is_game_over():
        draw_board(screen, board)

        if board.turn == chess.WHITE:
            # Player's move
            move = input("Enter your move (e.g., e2e4): ")
            move = chess.Move.from_uci(move)
            if move in board.legal_moves:
                board.push(move)
            else:
                print("Invalid move. Try again.")
        else:
            # AI's move using Stockfish
            print("AI is thinking...")
            with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
                result = engine.play(board, chess.engine.Limit(time=2.0))  # AI plays with a 2-second time limit
                ai_move = result.move
                print(f"AI plays: {ai_move}")
                board.push(ai_move)

        p.display.flip()
        clock.tick(MAX_FPS)

    print(f"Game Over. Result: {board.result()}")

if __name__ == "__main__":
    play_vs_ai()
