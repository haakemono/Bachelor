import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Database')))

import database

def change_password():
    """Handles password change for a logged-in user."""
    print("\n--- Change Password ---")
    
    try:
        with open("user_info.txt", "r") as file:
            username = file.read().strip()
    except FileNotFoundError:
        print("No user is logged in. Please log in first.")
        return
    
    old_password = input("Enter your current password: ").strip()
    if not database.login_user(username, old_password):
        print("Incorrect current password. Try again.")
        return
    
    new_password = input("Enter your new password: ").strip()
    confirm_password = input("Confirm your new password: ").strip()
    
    if new_password != confirm_password:
        print("Passwords do not match. Try again.")
        return
    
    conn, cursor = database.connect_db()
    hashed_new_password = database.hash_password(new_password)
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (hashed_new_password, username))
    conn.commit()
    conn.close()
    
    print("Password changed successfully!")

if __name__ == "__main__":
    change_password()