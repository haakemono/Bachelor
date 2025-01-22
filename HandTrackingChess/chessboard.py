import pygame
import chess

class ChessBoard:
    def __init__(self, engine, assets_path, square_size):
        self.engine = engine
        self.assets_path = assets_path
        self.square_size = square_size
        self.piece_images = self._load_piece_images()

    def _load_piece_images(self):
        # Load images for all pieces (e.g., 'wk.png' for white king)
        pieces = ["k", "q", "r", "b", "n", "p"]
        colors = ["w", "b"]
        piece_images = {}
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece}"
                path = f"{self.assets_path}/{key}.png"
                try:
                    piece_images[key] = pygame.image.load(path)
                    # Scale the image to fit the square size
                    piece_images[key] = pygame.transform.scale(piece_images[key], (self.square_size, self.square_size))
                except pygame.error as e:
                    print(f"Error loading image for {key}: {e}")
        return piece_images


    def draw(self, screen):
        for row in range(8):
            for col in range(8):
                # Draw the board squares
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(screen, (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71), rect)

                # Convert (row, col) to square index
                square = chess.square(col, 7 - row)  # Convert to chess board indexing

                # Get the piece on the square
                piece = self.engine.board.piece_at(square)
                if piece:
                    piece_key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"  # e.g., 'wp', 'bn'
                    piece_image = self.piece_images.get(piece_key)
                    if piece_image:
                        screen.blit(piece_image, rect.topleft)

