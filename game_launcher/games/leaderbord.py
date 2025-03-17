from database import get_scores

def display_leaderboard():
    print("\n=== Global Leaderboard ===")
    scores = get_scores()
    if not scores:
        print("No scores available yet!")
        return

    for idx, (user, score) in enumerate(scores, 1):
        print(f"{idx}. {user}: {score} points")

if __name__ == "__main__":
    display_leaderboard()
