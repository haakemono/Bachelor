import pygame
import os
import sys

# Print the current working directory (where the script is running)
print(f"🔍 Current Working Directory: {os.getcwd()}")

# Get the absolute path of the project root directory (one level up)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Print the detected project root path
print(f"📂 Detected Project Root: {PROJECT_ROOT}")

# Add the project root to Python's module search path
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
    print(f"✅ Added to sys.path: {PROJECT_ROOT}")

# Check what paths Python is using to look for modules
print(f"🔍 sys.path:\n{sys.path}")

# Now, try importing Database
try:
    from Database.database import get_logged_in_user, logout_user
    print("✅ Successfully imported Database module!")
except ModuleNotFoundError as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)  # Stop execution if import fails





# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selection Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (100, 200, 255)

# Font settings
font = pygame.font.Font(None, 50)

# Define absolute paths for the scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Now inside Meny/
ROOT_DIR = os.path.dirname(BASE_DIR)  # Go one level up to the main project folder

games = [
    {"name": "Memory Game", "folder": "Gestures", "script": "memory_game.py"},
    {"name": "Apple Catching", "folder": "AppleCatcher", "script": "game.py"},
    {"name": "Chess", "folder": "Chess", "script": "main.py"},
    {"name": "Log Out", "folder": None, "script": None},
    {"name": "Exit", "folder": None, "script": None}
]

def draw_menu(selected_index, username):
    """Render the menu on screen"""
    screen.fill(WHITE)

    title_text = font.render(f"Logged in as: {username}", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    for i, game in enumerate(games):
        color = HIGHLIGHT if i == selected_index else BLACK
        text = font.render(game["name"], True, color)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200 + i * 80))

    pygame.display.flip()

def launch_game(folder, script, username):
    """Change working directory to game folder and launch game with username argument"""
    if folder and script:
        game_path = os.path.join(ROOT_DIR, folder, script)
        game_dir = os.path.join(ROOT_DIR, folder)

        print(f"🔹 Launching {script} from {folder} as {username}")

        os.chdir(game_dir)  
        os.execv(sys.executable, ["python", script, username])  # Pass username to game

def main():
    """Main menu loop"""
    username = get_logged_in_user()  # Get logged-in user

    if not username:  # If no user is logged in, redirect to login
        print("🔒 No user logged in. Redirecting to login...")
        os.execv(sys.executable, ["python", os.path.join(BASE_DIR, "log_in.py")])

    selected_index = 0
    running = True

    while running:
        draw_menu(selected_index, username)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(games)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(games)
                elif event.key == pygame.K_RETURN:
                    folder = games[selected_index]["folder"]
                    script = games[selected_index]["script"]
                    
                    if games[selected_index]["name"] == "Log Out":
                        logout_user()
                        os.execv(sys.executable, ["python", os.path.join(BASE_DIR, "log_in.py")])  # Log out and redirect to login
                    elif script:
                        launch_game(folder, script, username)
                    else:
                        running = False  # Exit menu

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
