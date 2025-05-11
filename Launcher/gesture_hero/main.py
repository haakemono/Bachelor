import pygame
import json
import os
from constants import WIDTH, HEIGHT, NOTE_SPEED, HIT_ZONE_X, HIT_TOLERANCE
from game_logic import generate_notes, check_hit
from render import draw_pause_menu, draw_screen, draw_game_over, draw_start_menu, draw_song_menu
from gesture_input import get_gesture_keypress, release_gesture_resources
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Hero")

def load_songs():
    #loads available songs from the JSON file
    base_path = os.path.dirname(__file__)  # gesture_hero/
    songs_path = os.path.join(base_path, "songs.json")
    with open(songs_path, "r") as f:
        data = json.load(f)
    return data["songs"]

def start_menu():
    #handles the transition from the start menu to song selection
    while True:
        draw_start_menu(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return song_selection_menu()  

def song_selection_menu():
    #displays the song selection menu and lets the user choose a song
    songs = load_songs()
    selected_song = 0  
    while True:
        draw_song_menu(WIN, songs, selected_song)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_song = (selected_song - 1) % len(songs)  
                if event.key == pygame.K_DOWN:
                    selected_song = (selected_song + 1) % len(songs) 
                if event.key == pygame.K_RETURN:
                    return songs[selected_song]  

def start_music(song_file):
    #plays the selected song immediately."
    full_path = os.path.join(os.path.dirname(__file__), song_file)
    pygame.mixer.init()
    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()

def game_loop(selected_song):
    #main game loop
    from gesture_input import get_gesture_keypress, release_gesture_resources

    notes = generate_notes(selected_song["beatmap"])  
    score = 0
    running = True
    frame_counter = 0

    song_start_time = pygame.time.get_ticks()
    start_music(selected_song["file"])  

    while running:
        current_time = pygame.time.get_ticks() - song_start_time
        draw_screen(WIN, notes, score, HIT_ZONE_X)

        #event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                release_gesture_resources()
                exit()
            if event.type == pygame.KEYDOWN: #handle keybind events
                if event.key == pygame.K_p:
                    action = pause_menu()
                    if action == "menu":
                        return "menu"
                    if action == "exit":
                        pygame.quit()
                        release_gesture_resources()
                        exit()
                else:
                    result = check_hit(event.key, notes, HIT_ZONE_X, HIT_TOLERANCE)
                    score += result
                    key_char = pygame.key.name(event.key).upper()
                    if result > 0:
                        print(f"Hit: {key_char} | Score: {score}")
                    else:
                        print(f"Missed: {key_char} | Score: {score}")

        #gesture every frame, but only when notes are within hit zone
        gesture_active = any(
            not note["hit"] and abs(note["x"] - HIT_ZONE_X) <= HIT_TOLERANCE
            for note in notes
        )
        if gesture_active:
            gesture_key = get_gesture_keypress()
            if gesture_key:
                result = check_hit(gesture_key, notes, HIT_ZONE_X, HIT_TOLERANCE)
                score += result
                key_char = pygame.key.name(gesture_key).upper()
                if result > 0:
                    print(f" Gesture Hit: {key_char} | Score: {score}")
                else:
                    print(f"Gesture Missed: {key_char} | Score: {score}")

        #move notes
        for note in notes:
            if not note["hit"] and note["time"] <= current_time: #prevent multiple hits for same note
                note["x"] -= NOTE_SPEED #move note towards left 
            if note["x"] < HIT_ZONE_X - HIT_TOLERANCE and not note["hit"]:  #if note is hit correctly slighlty after passing the hit zone, it COULD still reward a point, the threshold can be changed in constants.py
                note["hit"] = True #mark note as missed
        
        if all(note["hit"] for note in notes):
            running = False

        pygame.time.delay(30)
        frame_counter += 1

    return game_over_loop(score, selected_song)



def pause_menu():
    #displays the pause menu and waits for input.
    pygame.mixer.music.pause()
    while True:
        draw_pause_menu(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    return "resume"  
                if event.key == pygame.K_m:
                    return "menu" 

def game_over_loop(score, selected_song):
    #displays the game over screen and waits for restart or song selection
    pygame.mixer.music.stop()
    while True:
        draw_game_over(WIN, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                release_gesture_resources()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return game_loop(selected_song)  
                if event.key == pygame.K_m:
                    return "menu"  

while True:
    selected_song = start_menu()
    if selected_song:
        result = game_loop(selected_song)
        if result == "menu":
            continue  
    break
release_gesture_resources()


