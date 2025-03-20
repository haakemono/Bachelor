import pygame
import chess

class ChessBoard:
    def __init__(self, engine, assets_path, square_size):
        self.engine = engine
        self.assets_path = assets_path
        self.square_size = square_size
        self.piece_images = self._load_piece_images()
        self.font = pygame.font.Font(None, 28)

    def _load_piece_images(self):
        pieces = ["k", "q", "r", "b", "n", "p"]
        colors = ["w", "b"]
        piece_images = {}
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece}"
                path = f"{self.assets_path}/{key}.png"
                try:
                    image = pygame.image.load(path)
                    image = pygame.transform.scale(image, (self.square_size, self.square_size))
                    piece_images[key] = image
                except pygame.error as e:
                    print(f"[ERROR] Could not load image for {key}: {e}")
        return piece_images

    def draw(self, screen):
        board_size = self.square_size * 8

        for row in range(8):
            for col in range(8):
                rect = pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                color = (255, 206, 158) if (row + col) % 2 == 0 else (209, 139, 71)
                pygame.draw.rect(screen, color, rect)

                square = chess.square(col, 7 - row)
                piece = self.engine.board.piece_at(square)
                if piece:
                    key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
                    piece_image = self.piece_images.get(key)
                    if piece_image:
                        screen.blit(piece_image, rect.topleft)

        for row in range(8):
            label = self.font.render(str(8 - row), True, (255, 255, 255))
            screen.blit(label, (5, row * self.square_size + self.square_size // 3))

        letters = "ABCDEFGH"
        for col in range(8):
            label = self.font.render(letters[col], True, (255, 255, 255))
            label_rect = label.get_rect(center=(col * self.square_size + self.square_size // 2, board_size + 5))
            screen.blit(label, label_rect)