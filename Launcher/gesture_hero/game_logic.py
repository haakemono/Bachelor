import os
import random
from constants import KEYS, TOTAL_NOTES, HEIGHT, WIDTH, HIT_TOLERANCE, HIT_ZONE_X


def load_beatmap(filename):
    #loads beatmap from a file and returns a list of notes with their timestamps
    filepath = os.path.join(os.path.dirname(__file__), filename)  #ensure correct path
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: {filepath} not found!")  #error message if missing
    
    notes = []
    with open(filepath, "r") as f:
        for line in f:
            timestamp, key = line.strip().split()
            notes.append({"time": int(timestamp), "key": KEYS[key], "x": WIDTH, "y": HEIGHT // 2, "hit": False}) #append notes from beatmap
    return notes
    
def generate_notes(beatmap_file):
    #loads notes based on beatmap
    return load_beatmap(beatmap_file)
    

def check_hit(event_key, notes, hit_zone_x, hit_tolerance):
    #checks if a note is hit correctly
    score = 0
    for note in notes:
        if not note["hit"] and note["key"] == event_key:
            # In check_hit()
            if hit_zone_x - HIT_TOLERANCE <= note["x"] <= hit_zone_x + HIT_TOLERANCE:
                score += 1
                note["hit"] = True  # mark the note as hit
    return score
