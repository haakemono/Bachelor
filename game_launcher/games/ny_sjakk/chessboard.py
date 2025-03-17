import pygame
import chess

class ChessBoard:
    def __init__(self, engine, assets_path, square_size):
        self.engine = engine
        self.assets_path = assets_path
        self.square_size = square_size
        self.piece_images = self._load_piece_images()
        self.font = pygame.font.Font(None, 28)  # Adjusted font size for better visibility

    def _load_piece_images(self):
        import os
        pieces = ["k", "q", "r", "b", "n", "p"]
        colors = ["w", "b"]
        piece_images = {}
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece}"
                path = os.path.join(self.assets_path, f"{key}.png")
                try:
                    piece_images[key] = pygame.image.load(path)
                    piece_images[key] = pygame.transform.scale(piece_images[key], (self.square_size, self.square_size))
                except pygame.error as e:
                    print(f"Error loading image for {key}: {e}")
        return piece_images


    def draw(self, screen):
        board_size = self.square_size * 8

        # Draw chessboard squares
        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(screen, (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71), rect)

                # Convert (row, col) to square index
                square = chess.square(col, 7 - row)

                # Draw piece if present
                piece = self.engine.board.piece_at(square)
                if piece:
                    piece_key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                    piece_image = self.piece_images.get(piece_key)
                    if piece_image:
                        screen.blit(piece_image, rect.topleft)

        # Draw row numbers (1-8) on the left side
        for row in range(8):
            text = self.font.render(str(8 - row), True, (255, 255, 255))
            screen.blit(text, (5, row * self.square_size + self.square_size // 3))  # Adjusted positioning

        # Draw column letters (A-H) below the board
        letters = "ABCDEFGH"
        for col in range(8):
            text = self.font.render(letters[col], True, (255, 255, 255))
            text_rect = text.get_rect(center=(col * self.square_size + self.square_size // 2, board_size + 5))
            screen.blit(text, text_rect)
