import pygame
from Constants import ASSETS_PATH, SQUARE_SIZE, SCREEN_SIZE, BAR_WIDTH, HOVER_TIME_THRESHOLD, STOCKFISH_PATH

class EvaluationBar:
    def __init__(self, screen, x_position, height, width=20):
        """
        Initialize the evaluation bar.
        
        Args:
            screen (pygame.Surface): The screen to draw the evaluation bar on.
            x_position (int): The x-coordinate where the evaluation bar will be drawn.
            height (int): The total height of the evaluation bar.
            width (int): The width of the evaluation bar.
        """
        self.screen = screen
        self.x_position = x_position
        self.height = height
        self.width = width

    def draw(self, evaluation):
        """
        Draw the evaluation bar based on the evaluation score.

        Args:
            evaluation (float): The evaluation score (positive for white, negative for black).
        """
        # Normalize the evaluation to fit between -1 (black winning) and 1 (white winning)
        normalized_eval = max(min(evaluation / 10, 1), -1)

        # Calculate white and black bar heights
        white_height = int((1 + normalized_eval) * self.height // 2)
        black_height = self.height - white_height

        # Define colors
        white_color = (255, 255, 255)  # White
        black_color = (0, 0, 0)        # Black

        # Draw black (bottom part)
        black_rect = pygame.Rect(self.x_position, self.height - black_height, self.width, black_height)
        pygame.draw.rect(self.screen, black_color, black_rect)

        # Draw white (top part)
        white_rect = pygame.Rect(self.x_position, 0, self.width, white_height)
        pygame.draw.rect(self.screen, white_color, white_rect)
