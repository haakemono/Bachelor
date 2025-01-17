import pygame
from constants import WIDTH, HEIGHT

def draw_window(win, bg, player, apples, bombs, score, true_score, accuracy, lives):
    """Draw the game window and its elements."""
    win.blit(bg, (0, 0))

    # Draw player
    pygame.draw.rect(win, "brown", (player.x, player.y, player.width, player.height))

    # Draw apples
    for apple in apples:
        pygame.draw.circle(win, "red", (apple["x"], apple["y"]), apple["radius"])

    # Draw bombs
    for bomb in bombs:
        pygame.draw.circle(win, "blue", (bomb["x"], bomb["y"]), bomb["radius"])

    # Display scores, accuracy, and lives
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, "black")
    true_score_text = font.render(f"Total apples: {true_score}", True, "black")
    accuracy_text = font.render(f"Accuracy: {accuracy:.1f}%", True, "black")  # Show accuracy percentage
    lives_text = font.render(f"Lives: {lives}", True, "black")

    win.blit(score_text, (10, 10))
    win.blit(true_score_text, (10, 40))
    win.blit(accuracy_text, (10, 70))  # Display accuracy below true score
    win.blit(lives_text, (10, 100))

    pygame.display.update()



def draw_fps(win, clock, font):
    """Draw the current FPS on the screen."""
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, "black")
    win.blit(fps_text, (WIDTH - 100, 10))
