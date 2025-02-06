import register
import log_in
import change_password
import log_out
import scores
import os

def is_logged_in():
    """Check if a user is logged in by reading user_info.txt."""
    return os.path.exists("user_info.txt") and os.path.getsize("user_info.txt") > 0

def get_logged_in_user():
    """Gets the username of the currently logged-in user."""
    if is_logged_in():
        with open("user_info.txt", "r") as file:
            return file.read().strip()
    return None

def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Register")
        print("2. Log In")

        if is_logged_in():
            print("3. Change Password")
            print("4. View Apple Catcher Score")
            print("5. Update Apple Catcher Score")
            print("6. View Memory Game Streak")
            print("7. Update Memory Game Streak")
            print("8. View Leaderboard")
            print("9. Log Out")
            print("10. Exit")
        else:
            print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register.register()
        elif choice == "2":
            log_in.log_in()
        elif is_logged_in() and choice == "3":
            change_password.change_password()
        elif is_logged_in() and choice == "4":
            scores.view_apple_catcher_score(get_logged_in_user())
        elif is_logged_in() and choice == "5":
            scores.update_apple_catcher_score(get_logged_in_user())
        elif is_logged_in() and choice == "6":
            scores.view_memory_game_streak(get_logged_in_user())
        elif is_logged_in() and choice == "7":
            scores.update_memory_game_streak(get_logged_in_user())
        elif is_logged_in() and choice == "8":
            scores.view_leaderboard()
        elif is_logged_in() and choice == "9":
            log_out.log_out()
        elif (is_logged_in() and choice == "10") or (not is_logged_in() and choice == "3"):
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
