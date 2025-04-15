from collections import deque

class DifficultyManager:
    def __init__(self):
        self.last_10_results = deque(maxlen=10)
        self.success_count = 0
        self.apple_fall_speed = 3
        self.new_apple_interval = 180
        self.new_bomb_interval = 300

    def track_performance(self, caught=False):
        """Update performance metrics efficiently."""
        if len(self.last_10_results) == 10:
            removed = self.last_10_results.popleft()
            self.success_count -= removed  # Remove old value from sum

        self.last_10_results.append(1 if caught else 0)
        self.success_count += (1 if caught else 0)  # Update running sum

    def calculate_recent_accuracy(self):
        """Calculate accuracy in O(1) time using precomputed sum."""
        if len(self.last_10_results) == 0:
            return 0
        return self.success_count / len(self.last_10_results)

    def adjust_difficulty(self):
        """Adjust game parameters based on last 10 apples' accuracy."""
        recent_accuracy = self.calculate_recent_accuracy()

        if recent_accuracy > 0.7:
            self.apple_fall_speed = min(10, self.apple_fall_speed + 5)
        elif recent_accuracy < 0.3:
            self.apple_fall_speed = max(3, self.apple_fall_speed - 0.1)

    def get_game_parameters(self):
        return {
            "apple_fall_speed": self.apple_fall_speed,
            "new_apple_interval": self.new_apple_interval,
            "new_bomb_interval": self.new_bomb_interval,
        }
