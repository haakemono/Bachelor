# --- chessboard.py ---
import pygame
import chess
import os

class ChessBoard:
    def __init__(self, engine, assets_path, square_size):
        self.engine = engine
        self.assets_path = assets_path
        self.square_size = square_size
        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq',
                  'bp', 'br', 'bn', 'bb', 'bk', 'bq']
        images = {}
        for piece in pieces:
            image_path = os.path.join(self.assets_path, f"{piece}.png")
            images[piece] = pygame.transform.scale(
                pygame.image.load(image_path), (self.square_size, self.square_size))
        return images

    def get_piece_image(self, piece):
        key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
        return self.piece_images.get(key)

    def draw(self, screen, skip_square=None):
        self.draw_board(screen)
        self.draw_pieces(screen, skip_square=skip_square)


    def draw_board(self, screen):
        colors = [pygame.Color("#f0d9b5"), pygame.Color("#b58863")]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen, color,
                    pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                )

    def draw_pieces(self, screen, skip_square=None):
        board = self.engine.board
        for square in chess.SQUARES:
            if square == skip_square:
                continue  # Skip drawing the animated piece’s old position
            piece = board.piece_at(square)
            if piece:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                piece_image = self.get_piece_image(piece)
                if piece_image:
                    screen.blit(piece_image, (col * self.square_size, row * self.square_size))


    def animate_move(self, screen, start_square, end_square, piece_image=None, duration=0.5):
        start_file = chess.square_file(start_square)
        start_rank = 7 - chess.square_rank(start_square)
        end_file = chess.square_file(end_square)
        end_rank = 7 - chess.square_rank(end_square)

        start_pos = (start_file * self.square_size, start_rank * self.square_size)
        end_pos = (end_file * self.square_size, end_rank * self.square_size)

        if not piece_image:
            piece = self.engine.get_piece_at(start_square)
            piece_image = self.get_piece_image(piece)

        frames = int(duration * 60)
        for frame in range(frames):
            t = frame / frames
            x = int(start_pos[0] + (end_pos[0] - start_pos[0]) * t)
            y = int(start_pos[1] + (end_pos[1] - start_pos[1]) * t)

            screen.fill((0, 0, 0))
            self.draw(screen, skip_square=start_square)  # Don't draw old position
            if piece_image:
                screen.blit(piece_image, (x, y))
            pygame.display.flip()
            pygame.time.delay(int(1000 / 60))
