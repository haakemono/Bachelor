import os
import random
from constants import KEYS, TOTAL_NOTES, HEIGHT, WIDTH


def load_beatmap(filename):
    """Loads beatmap from a file and returns a list of notes with their timestamps."""
    filepath = os.path.join(os.path.dirname(__file__), filename)  # ✅ Ensure correct path
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: {filepath} not found!")  # ✅ Error message if missing
    
    notes = []
    with open(filepath, "r") as f:
        for line in f:
            timestamp, key = line.strip().split()
            notes.append({"time": int(timestamp), "key": KEYS[key], "x": WIDTH, "y": HEIGHT // 2, "hit": False})
    return notes
    
def generate_notes(beatmap_file):
    "loads notes based on beatmap"
    return load_beatmap(beatmap_file)
    

def check_hit(event_key, notes, hit_zone_x, hit_tolerance):
    "checks if a note is hit correctly."
    score = 0
    for note in notes:
        if not note["hit"] and note["key"] == event_key:
            if abs(note["x"] - hit_zone_x) <= hit_tolerance:
                score += 1
                note["hit"] = True  # mark the note as hit
    return score
