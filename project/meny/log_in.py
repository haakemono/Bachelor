import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database')))

import database

def log_in():
    """Handles user login."""
    print("\n--- Log In ---")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    
    if database.login_user(username, password):
        print("Login successful!")
        with open("user_info.txt", "w") as file:
            file.write(username)
    else:
        print("Invalid username or password. Try again.")

if __name__ == "__main__":
    log_in()