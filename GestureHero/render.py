import pygame
from constants import GRAY, WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, BLUE, FONT


def draw_pause_menu(win):
    "displays pause menu with options"
    win.fill(BLACK)
    pause_text = FONT.render("PAUSED", True, RED)
    resume_text = FONT.render ("Press P to Resume", True, WHITE)
    menu_text = FONT.render("Press M for Main Menu", True, WHITE)

    win.blit(pause_text, (WIDTH // 2 - 80, HEIGHT // 2 - 80))
    win.blit(resume_text, (WIDTH // 2 - 140, HEIGHT // 2))
    win.blit(menu_text, (WIDTH // 2 - 160, HEIGHT // 2 + 40))

    pygame.display.flip()

def draw_start_menu(win):
    "displays the start menu before game begins"
    win.fill(BLACK)
    title_text = FONT.render("Gesture Hero", True, RED)
    instruction_text = FONT.render("Press SPACE to Start", True, WHITE)

    win.blit(title_text, (WIDTH // 2 - 150, HEIGHT // 2 - 80))
    win.blit(instruction_text, (WIDTH // 2 - 150, HEIGHT // 2))

    pygame.display.flip()

def draw_screen(win, notes, score, hit_zone_x):
    "draws the game screen with horizontal moving notes."
    win.fill(BLACK)

    # draw hit zone
    pygame.draw.rect(win, WHITE, (hit_zone_x, HEIGHT // 2 - 30, 10, 60))

    # draw notes
    for note in notes:
        if not note["hit"]:
            text = FONT.render(chr(note["key"]).upper(), True, BLUE)  # display key input
            win.blit(text, (note["x"], note["y"] - 20))  

    # display text
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    pause_text = FONT.render("Press P to Pause", True, WHITE)
    
    win.blit(score_text, (10, 10))  
    win.blit(pause_text, (WIDTH - 290, 10))  

    pygame.display.flip()
def draw_song_menu(win, songs, selected_index):
    "Draws the song selection menu."
    win.fill(BLACK)
    title_text = FONT.render("Select a Song", True, WHITE)
    win.blit(title_text, (WIDTH // 2 - 100, 50))

    for i, song in enumerate(songs):
        color = GREEN if i == selected_index else WHITE
        song_text = FONT.render(song["title"], True, color)
        win.blit(song_text, (WIDTH // 2 - 80, 150 + i * 50))

    instruction_text = FONT.render("UP/DOWN to Select, ENTER to Play", True, GRAY)
    win.blit(instruction_text, (WIDTH // 2 - 200, HEIGHT - 100))

    pygame.display.flip()

def draw_game_over(win, score):
    "displays the game over screen WITH restart button"
    win.fill(BLACK)
    game_over_text = FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"Final Score: {score}", True, WHITE)
    restart_text = FONT.render("Press R to Restart", True, GRAY)
    
    win.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 50))
    win.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    win.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 50))

    pygame.display.flip()

