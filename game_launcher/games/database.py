import sqlite3

# Initialize database and create the table
def init_db():
    conn = sqlite3.connect("user_scores.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_user(username):
    conn = sqlite3.connect("user_scores.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO user_scores (username, score) VALUES (?, ?)", (username, 0))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"User {username} already exists!")
    conn.close()

def update_score(username, points):
    conn = sqlite3.connect("user_scores.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user_scores SET score = score + ? WHERE username = ?", (points, username))
    conn.commit()
    conn.close()

def get_scores():
    conn = sqlite3.connect("user_scores.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM user_scores ORDER BY score DESC")
    scores = cursor.fetchall()
    conn.close()
    return scores

init_db()
