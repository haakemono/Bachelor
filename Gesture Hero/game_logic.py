import random
from constants import KEYS, TOTAL_NOTES, HEIGHT, WIDTH

def generate_notes():
    notes = []
    spacing = 150  

    for i in range(TOTAL_NOTES):
        key = random.choice(KEYS)  
        notes.append({
            "x": WIDTH + i * spacing,  # start off-screen and come in one at a time
            "y": HEIGHT // 2,   # centered vertically
            "key": key,
            "hit": False
        })
    
    return notes

def check_hit(event_key, notes, hit_zone_x, hit_tolerance):
    "checks if a note is hit correctly."
    score = 0
    for note in notes:
        if not note["hit"] and note["key"] == event_key:
            if abs(note["x"] - hit_zone_x) <= hit_tolerance:
                score += 1
                note["hit"] = True  # mark the note as hit
    return score
