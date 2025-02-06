import sqlite3
import hashlib
import os

# Get the absolute path to the database file
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "game_scores.db"))

def connect_db():
    """Connects to the SQLite database and returns the connection and cursor."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor

def create_table():
    """Creates the users table if it doesn't exist and ensures game-specific score columns are present."""
    conn, cursor = connect_db()

    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

    # Check for missing columns and add them
    cursor.execute("PRAGMA table_info(users);")
    columns = [column[1] for column in cursor.fetchall()]
    
    if "apple_catcher_highscore" not in columns:
        print("Adding 'apple_catcher_highscore' column to database...")
        cursor.execute("ALTER TABLE users ADD COLUMN apple_catcher_highscore INTEGER DEFAULT 0")
        conn.commit()

    if "memory_game_streak" not in columns:
        print("Adding 'memory_game_streak' column to database...")
        cursor.execute("ALTER TABLE users ADD COLUMN memory_game_streak INTEGER DEFAULT 0")
        conn.commit()

    conn.close()


def hash_password(password):
    """Hashes the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def user_exists(username):
    """Checks if a username already exists in the database."""
    conn, cursor = connect_db()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def register_user(username, password):
    """Registers a new user if the username is not taken."""
    if user_exists(username):
        return False  # Username already exists
    conn, cursor = connect_db()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password, score) VALUES (?, ?, ?)", (username, hashed_password, 0))
        conn.commit()
        return True
    finally:
        conn.close()

def login_user(username, password):
    """Checks if the username and password match a record in the database."""
    conn, cursor = connect_db()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    if record and record[0] == hash_password(password):
        return True
    return False

def update_score(username, new_score):
    """Updates the user's score."""
    conn, cursor = connect_db()
    cursor.execute("UPDATE users SET score = ? WHERE username = ?", (new_score, username))
    conn.commit()
    conn.close()

def get_score(username):
    """Retrieves the user's current score."""
    conn, cursor = connect_db()
    cursor.execute("SELECT score FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    return record[0] if record else None

def get_all_scores():
    """Retrieves all users' scores sorted in descending order (for leaderboard)."""
    conn, cursor = connect_db()
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC")
    scores = cursor.fetchall()
    conn.close()
    return scores

def update_apple_catcher_score(username, apples_caught):
    """Updates the highest apples caught in Apple Catcher."""
    conn, cursor = connect_db()
    cursor.execute("SELECT apple_catcher_highscore FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()

    if record and apples_caught > record[0]:  # Update only if the new score is higher
        cursor.execute("UPDATE users SET apple_catcher_highscore = ? WHERE username = ?", (apples_caught, username))
        conn.commit()

    conn.close()

def get_apple_catcher_score(username):
    """Retrieves the highest apples caught for Apple Catcher."""
    conn, cursor = connect_db()
    cursor.execute("SELECT apple_catcher_highscore FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    return record[0] if record else 0

def update_memory_game_streak(username, streak):
    """Updates the longest streak in the Memory Game."""
    conn, cursor = connect_db()
    cursor.execute("SELECT memory_game_streak FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()

    if record and streak > record[0]:  # Update only if the new streak is longer
        cursor.execute("UPDATE users SET memory_game_streak = ? WHERE username = ?", (streak, username))
        conn.commit()

    conn.close()

def get_memory_game_streak(username):
    """Retrieves the longest streak for the Memory Game."""
    conn, cursor = connect_db()
    cursor.execute("SELECT memory_game_streak FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    return record[0] if record else 0


# Initialize database when the module is loaded
create_table()
