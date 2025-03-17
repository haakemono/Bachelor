import pygame
import json
import os
from constants import WIDTH, HEIGHT, NOTE_SPEED, HIT_ZONE_X, HIT_TOLERANCE
from game_logic import generate_notes, check_hit
from render import draw_pause_menu, draw_screen, draw_game_over, draw_start_menu, draw_song_menu

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Hero")

def load_songs():
    "Loads available songs from the JSON file."
    with open("songs.json", "r") as f:
        data = json.load(f)
    return data["songs"]

def start_menu():
    "Handles the transition from the start menu to song selection."
    while True:
        draw_start_menu(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return song_selection_menu()  

def song_selection_menu():
    "Displays the song selection menu and lets the user choose a song."
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
    "Plays the selected song immediately."
    pygame.mixer.init()
    pygame.mixer.music.load(song_file)
    pygame.mixer.music.play()

def game_loop(selected_song):
    "Main game loop that runs until the song is finished."
    notes = generate_notes(selected_song["beatmap"])  
    score = 0
    running = True
    
    song_start_time = pygame.time.get_ticks()
    start_music(selected_song["file"])  

    while running:
        current_time = pygame.time.get_ticks() - song_start_time
        draw_screen(WIN, notes, score, HIT_ZONE_X)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    action = pause_menu()
                    if action == "menu":
                        return "menu"
                    if action == "exit":
                        pygame.quit()
                        exit()
                else:
                    score += check_hit(event.key, notes, HIT_ZONE_X, HIT_TOLERANCE)

        for note in notes:
            if not note["hit"] and note["time"] <= current_time:
                note["x"] -= NOTE_SPEED  
            if note["x"] < HIT_ZONE_X - 50 and not note["hit"]:
                note["hit"] = True 
        
        if all(note["hit"] for note in notes):
            running = False

        pygame.time.delay(30)

    return game_over_loop(score, selected_song)

def pause_menu():
    "Displays the pause menu and waits for input."
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
    "Displays the game over screen and waits for restart or song selection."
    pygame.mixer.music.stop()
    while True:
        draw_game_over(WIN, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
