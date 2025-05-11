# --- chessboard.py ---
import pygame
import chess
import os

"""#
Chessboard class for managing the visual chessboard.
It sets up the board with the engine, asset path, and square size,
loads and scale piece image and handles drawing piece and the board.
"""
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
            padding = 20
            images[piece] = pygame.transform.scale(
                pygame.image.load(image_path), (self.square_size- padding, self.square_size - padding))
        return images

    def get_piece_image(self, piece):
        key = f"{'w' if piece.color else 'b'}{piece.symbol().lower()}"
        return self.piece_images.get(key)

    def draw(self, screen, skip_square=None):
        self.draw_board(screen)
        self.draw_pieces(screen, skip_square=skip_square)
    """
    Draws the chessboard and adds custom ranks (bottom) and file (sides) labels to the screen
    """

    def draw_board(self, screen):
        colors = [pygame.Color("#f0d9b5"), pygame.Color("#b58863")]
        font = pygame.font.SysFont("Arial", 16)
        file_labels = ["P", "L", "K", "J", "I", "O", "X", "Y"]
        rank_labels = ["A", "B", "C", "D", "E", "F", "G", "H"]
        
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(
                    screen, color,
                    pygame.Rect(col * self.square_size, row * self.square_size, self.square_size, self.square_size)
                )
                if col == 0:
                    rank_label_text = file_labels[row]
                    rank_label = font.render(rank_label_text, True, pygame.Color("black"))
                    screen.blit(rank_label, (5, row * self.square_size + 5))

                # Draw custom file labels along bottom row
                if row == 7:
                    file_label_text = rank_labels[col]
                    file_label = font.render(file_label_text, True, pygame.Color("black"))
                    label_x = (col + 1) * self.square_size - font.size(file_label_text)[0] - 5
                    label_y = self.square_size * 8 - 18
                    screen.blit(file_label, (label_x, label_y))
                
    """
    Draws all chess pieces on the board
    Each piece image is centered within its square using padding
    """
    def draw_pieces(self, screen, skip_square=None):
        board = self.engine.board
        for square in chess.SQUARES:
            if square == skip_square:
                continue  
            piece = board.piece_at(square)
            if piece:
                row = 7 - chess.square_rank(square)
                col = chess.square_file(square)
                piece_image = self.get_piece_image(piece)
                if piece_image:
                    padding = (self.square_size - piece_image.get_width()) //2
                    screen.blit(piece_image, (col * self.square_size + padding, row * self.square_size + padding))

        """
        Animates a piece moving from one square to another.
        The board is redrawn each frame, and the piece position is updated step by step.
        """
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
            self.draw(screen, skip_square=start_square)  
            if piece_image:
                offset_x = (self.square_size - piece_image.get_width()) // 2
                offset_y = (self.square_size - piece_image.get_height()) // 2
                screen.blit(piece_image, (x +offset_x, y + offset_y))
            pygame.display.flip()
            pygame.time.delay(int(1000 / 60))
