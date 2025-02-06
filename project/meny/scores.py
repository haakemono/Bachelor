import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database')))

import database

def view_apple_catcher_score(username):
    """Displays the highest apples caught in Apple Catcher."""
    score = database.get_apple_catcher_score(username)
    print(f"\nYour highest apples caught: {score}")

def update_apple_catcher_score(username):
    """Allows the user to update their Apple Catcher high score."""
    try:
        new_score = int(input("Enter your new Apple Catcher score: "))
        database.update_apple_catcher_score(username, new_score)
        print("\nApple Catcher high score updated!")
    except ValueError:
        print("\nInvalid input! Please enter a valid number.")

def view_memory_game_streak(username):
    """Displays the longest streak in the Memory Game."""
    streak = database.get_memory_game_streak(username)
    print(f"\nYour longest streak in the Memory Game: {streak}")

def update_memory_game_streak(username):
    """Allows the user to update their Memory Game longest streak."""
    try:
        new_streak = int(input("Enter your new Memory Game streak: "))
        database.update_memory_game_streak(username, new_streak)
        print("\nMemory Game streak updated!")
    except ValueError:
        print("\nInvalid input! Please enter a valid number.")

def view_leaderboard():
    """Displays the leaderboard sorted by Apple Catcher scores and Memory Game streaks."""
    print("\n--- Apple Catcher Leaderboard ---")
    users = database.get_all_scores()  # You can modify this to show Apple Catcher scores
    for rank, (user, _) in enumerate(users, start=1):
        apples = database.get_apple_catcher_score(user)
        print(f"{rank}. {user} - {apples} apples")

    print("\n--- Memory Game Leaderboard ---")
    for rank, (user, _) in enumerate(users, start=1):
        streak = database.get_memory_game_streak(user)
        print(f"{rank}. {user} - {streak} streak")
