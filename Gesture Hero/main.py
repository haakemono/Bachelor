import pygame
from constants import WIDTH, HEIGHT, NOTE_SPEED, HIT_ZONE_X, HIT_TOLERANCE
from game_logic import generate_notes, check_hit
from render import draw_pause_menu, draw_screen, draw_game_over, draw_start_menu

# init pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Hero")

def start_menu():
    "displays the start menu and waits for the player to start"
    while True:
        draw_start_menu(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return 
    

def pause_menu():
    "displas the pause menu and waits for input"
    while True:
        draw_pause_menu(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    return "resume"  
                if event.key == pygame.K_m:
                    return "menu" 


def game_loop():
    "main game loop that runs until song is finished"
        # generate notes
    notes = generate_notes()
    score = 0
    running = True

    while running:
        draw_screen(WIN, notes, score, HIT_ZONE_X)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    action = pause_menu()
                    if action == "menu":
                        return "menu"
                    if action == "exit":
                        pygame.quit()
                        return
                    
                else:
                    score += check_hit(event.key, notes, HIT_ZONE_X, HIT_TOLERANCE)

        # notes coming horizontally
        for note in notes:
            if not note["hit"]:
                note["x"] -= NOTE_SPEED  # move left

            #mark notes as missed
            if note ["x"] < HIT_ZONE_X - 50 and not note ["hit"]:
                note["hit"] = True 

        # check for all notes played
        if all(note["hit"] for note in notes):
            running = False

        pygame.time.delay(30)

    return game_over_loop (score)

def game_over_loop(score):
    "displays game over screen and waits for restart button to be pressed"
    while True:

        draw_game_over(WIN, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                if event.key == pygame.K_m:
                    return "menu"

while True:
    start_menu()
    result = game_loop()

    if result == "menu":
        continue
           
