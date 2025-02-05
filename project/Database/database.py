import sqlite3
import os

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game_scores.db")

def connect_db():
    """Connect to the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        logged_in INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(username, password):
    """Log in a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET logged_in = 1 WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def logout_user():
    """Log out the current user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET logged_in = 0")
    conn.commit()
    conn.close()

def get_logged_in_user():
    """Get the currently logged-in user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE logged_in = 1")
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

def change_password(username, old_password, new_password):
    """Change the user's password."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET password = ? WHERE username = ? AND password = ?", (new_password, username, old_password))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success

# Initialize database
connect_db()
