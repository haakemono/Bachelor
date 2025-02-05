from Database.database import change_password

def main():
    print("🔑 Change your password")
    username = input("Enter your username: ").strip()
    old_password = input("Enter your current password: ").strip()
    new_password = input("Enter your new password: ").strip()
    
    if change_password(username, old_password, new_password):
        print("✅ Password updated successfully!")
    else:
        print("❌ Incorrect current password or user does not exist.")

    input("Press Enter to return to login.")
    import os, sys
    os.execv(sys.executable, ["python", "Meny/log_in.py"])

if __name__ == "__main__":
    main()
