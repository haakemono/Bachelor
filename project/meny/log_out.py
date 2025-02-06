import os

def log_out():
    """Logs out the current user by clearing the user_info.txt file."""
    if os.path.exists("user_info.txt"):
        with open("user_info.txt", "w") as file:
            file.write("")  # Clear file contents
        print("\nSuccessfully logged out!")
    else:
        print("\nNo user is currently logged in.")
