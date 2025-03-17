import pygame
from constants import FONT, GRAY, WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, BLUE, PURPLE
import os

BASE_PATH = os.path.dirname(__file__)
FONT = pygame.font.Font(os.path.join(BASE_PATH, "assets", "futuristic.otf"), 36)


# game backgrounds
background = pygame.image.load(os.path.join(BASE_PATH, "assets", "background.png"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  
background_x = 0  # Background scrolling position

main_menu_background = pygame.image.load(os.path.join(BASE_PATH, "assets", "mainmenu.png"))
main_menu_background = pygame.transform.scale(main_menu_background, (WIDTH, HEIGHT))

start_texture = pygame.image.load(os.path.join(BASE_PATH, "assets", "startbutton.png"))
start_texture = pygame.transform.scale(start_texture, (200, 200))  # Adjust size if needed

# load selection menu
level_selection_bg = pygame.image.load(os.path.join(BASE_PATH, "assets", "levelselection.png"))
level_selection_bg = pygame.transform.scale(level_selection_bg, (WIDTH, HEIGHT))

last_key_press_time = None
hit_zone_color = WHITE
flash_effect_time = None

def draw_pause_menu(win):
    """Displays the pause menu with options, ensuring all text is centered."""
    win.fill(BLACK)
    
    pause_text = FONT.render("PAUSED", True, RED)
    resume_text = FONT.render("PRESS P TO RESUME", True, PURPLE)
    menu_text = FONT.render("PRESS M FOR MAIN MENU", True, PURPLE)
    
    pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80))
    resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    
    win.blit(pause_text, pause_rect)
    win.blit(resume_text, resume_rect)
    win.blit(menu_text, menu_rect)
    
    pygame.display.flip()
def draw_start_menu(win):
    "Displays the start menu before the game begins."
    win.blit(main_menu_background, (0, 0))  
    win.blit(start_texture, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
    pygame.display.flip()

def draw_song_menu(win, songs, selected_index):
    "Displays the level selection menu with song options."
    win.blit(level_selection_bg, (0, 0))  
    # Display song options
    for i, song in enumerate(songs):
        color = PURPLE if i == selected_index else WHITE
        song_text = FONT.render(song["title"], True, color)
        win.blit(song_text, (WIDTH // 2 - 80, 200 + i * 50))  
    
    instruction_text = FONT.render("UP/DOWN to Select, ENTER to Play", True, PURPLE)
    win.blit(instruction_text, (WIDTH // 2 - 450, HEIGHT - 160))  
    
    pygame.display.flip()

def draw_screen(win, notes, score, hit_zone_x, key_pressed=None):
    "Draws the game screen with horizontal moving notes."
    global last_key_press_time, hit_zone_color, flash_effect_time, background_x
    current_time = pygame.time.get_ticks()

    background_x -= 1
    if background_x <= -WIDTH:
        background_x = 0
    win.blit(background, (background_x, 0))
    win.blit(background, (background_x + WIDTH, 0))
    
    if key_pressed:
        for note in notes:
            if not note["hit"] and abs(note["x"] - hit_zone_x) <= 20:
                if chr(note["key"]).lower() == key_pressed:
                    hit_zone_color = (255, 255, 0)
                    last_key_press_time = current_time
                    note["hit"] = True
                    break  
    
    if last_key_press_time and current_time - last_key_press_time > 500:
        hit_zone_color = WHITE
        last_key_press_time = None
    
    pygame.draw.rect(win, hit_zone_color, (hit_zone_x, HEIGHT // 2 - 30, 10, 60))
    
    for note in notes:
        if not note["hit"]:
            text = FONT.render(chr(note["key"]).upper(), True, BLUE)
            win.blit(text, (note["x"], note["y"] - 20))  
    
    score_text = FONT.render(f"Score: {score}", True, PURPLE)
    pause_text = FONT.render("Press P to Pause", True, PURPLE)
    
    win.blit(score_text, (10, 10))  
    win.blit(pause_text, (WIDTH - 475, 10))
    
    pygame.display.flip()

def draw_game_over(win, score):
    """Displays the game over screen with centered text."""
    win.fill(BLACK)
    
    game_over_text = FONT.render("GAME OVER", True, RED)
    score_text = FONT.render(f"FINAL SCORE: {score}", True, PURPLE)
    restart_text = FONT.render("PRESS R TO RESTART", True, PURPLE)
    
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    win.blit(game_over_text, game_over_rect)
    win.blit(score_text, score_rect)
    win.blit(restart_text, restart_rect)
    
    pygame.display.flip()
