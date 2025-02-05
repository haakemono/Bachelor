from Database.database import register_user

def main():
    print("🔹 Register a new user")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    
    if register_user(username, password):
        print("✅ Registration successful!")
    else:
        print("❌ Username already exists.")
    
    input("Press Enter to return to login.")
    import os, sys
    os.execv(sys.executable, ["python", "Meny/log_in.py"])

if __name__ == "__main__":
    main()
