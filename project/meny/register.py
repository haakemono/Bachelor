import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database')))

import database

def register():
    """Handles user registration."""
    print("\n--- Register a New Account ---")
    username = input("Enter a username: ").strip()
    password = input("Enter a password: ").strip()
    confirm_password = input("Confirm your password: ").strip()
    
    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return
    
    if database.register_user(username, password):
        print("Registration successful! You can now log in.")
    else:
        print("Username already exists. Choose a different one.")

if __name__ == "__main__":
    register()
