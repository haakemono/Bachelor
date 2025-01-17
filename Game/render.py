import pygame
from constants import WIDTH, HEIGHT

def draw_window(win, bg, player, apples, bombs, score, lives):
    """Draw the game window and its elements."""
    win.blit(bg, (0, 0))

    # Draw player
    pygame.draw.rect(win, "brown", player)  # player is now a pygame.Rect

    # Draw apples
    for apple in apples:
        pygame.draw.circle(win, "red", (apple["x"], apple["y"]), apple["radius"])

    # Draw bombs
    for bomb in bombs:
        pygame.draw.circle(win, "blue", (bomb["x"], bomb["y"]), bomb["radius"])

    # Display score and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, "black")
    lives_text = font.render(f"Lives: {lives}", True, "black")
    win.blit(score_text, (10, 10))
    win.blit(lives_text, (10, 40))

    pygame.display.update()


def draw_fps(win, clock, font):
    """Draw the current FPS on the screen."""
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, "black")
    win.blit(fps_text, (WIDTH - 100, 10))
