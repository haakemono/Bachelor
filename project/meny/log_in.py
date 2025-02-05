import sys
import os

# Get the project root directory (one level up from 'meny/')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the project root to the system path so Python finds 'Database'
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from Database.database import login_user

def main():
    print("🔒 Log in to your account")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if login_user(username, password):
        print("✅ Login successful!")
        import os, sys
        os.execv(sys.executable, ["python", "Meny/menu.py"])  # Redirect to menu
    else:
        print("❌ Incorrect username or password.")
        choice = input("Try again? (Y/N): ").strip().lower()
        if choice == "y":
            main()
        else:
            print("Returning to menu.")

if __name__ == "__main__":
    main()
