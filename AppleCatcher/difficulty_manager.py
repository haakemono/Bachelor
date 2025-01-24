from collections import deque

class DifficultyManager:
    def __init__(self):
        # Track performance metrics
        self.last_10_results = deque(maxlen=10)  # Store results of the last 10 apples
        self.apple_fall_speed = 3
        self.new_apple_interval = 180
        self.new_bomb_interval = 300

    def track_performance(self, caught=False):
        """Update performance metrics."""
        self.last_10_results.append(1 if caught else 0)

    def calculate_recent_accuracy(self):
        """Calculate accuracy for the last 10 apples."""
        if len(self.last_10_results) == 0:
            return 0
        return sum(self.last_10_results) / len(self.last_10_results)

    def adjust_difficulty(self):
        """Adjust game parameters based on the last 10 apples' accuracy."""
        recent_accuracy = self.calculate_recent_accuracy()

        if recent_accuracy > 0.7:  # High accuracy
            self.apple_fall_speed = min(10, self.apple_fall_speed + 5)
        elif recent_accuracy < 0.3:  # Low accuracy
            self.apple_fall_speed = max(3, self.apple_fall_speed - 0.1)

    def get_game_parameters(self):
        """Return the current game parameters."""
        return {
            "apple_fall_speed": self.apple_fall_speed,
            "new_apple_interval": self.new_apple_interval,
            "new_bomb_interval": self.new_bomb_interval,
        }
