class DifficultyManager:
    def __init__(self):
        # Track performance metrics
        self.apples_caught = 0
        self.apples_spawned = 0
        self.reaction_times = []

        # Initial game parameters
        self.apple_fall_speed = 3
        self.new_apple_interval = 180
        self.new_bomb_interval = 300

    def track_performance(self, caught=False, reaction_time=None):
        """Update performance metrics."""
        if caught:
            self.apples_caught += 1
            if reaction_time is not None:
                self.reaction_times.append(reaction_time)
        self.apples_spawned += 1

    def calculate_accuracy(self):
        """Calculate player's accuracy."""
        if self.apples_spawned == 0:
            return 0
        return self.apples_caught / self.apples_spawned

    def calculate_average_reaction_time(self):
        """Calculate the average reaction time."""
        if not self.reaction_times:
            return 2.0  # Default slower reaction time
        return sum(self.reaction_times) / len(self.reaction_times)

    def adjust_difficulty(self):
        """Adjust game parameters based on performance."""
        accuracy = self.calculate_accuracy()
        avg_reaction_time = self.calculate_average_reaction_time()

        # Adjust based on accuracy
        if accuracy > 0.7:  # High accuracy
            self.apple_fall_speed = min(10, self.apple_fall_speed + 0.1)
            self.new_apple_interval = max(90, self.new_apple_interval - 2)
            self.new_bomb_interval = max(200, self.new_bomb_interval - 5)
        elif avg_reaction_time < 1.5:  # Fast reactions
            self.apple_fall_speed = min(10, self.apple_fall_speed + 0.05)
            self.new_apple_interval = max(100, self.new_apple_interval - 1)
        else:  # Low accuracy or slow reactions
            self.apple_fall_speed = max(3, self.apple_fall_speed - 0.05)
            self.new_apple_interval = min(300, self.new_apple_interval + 1)
            self.new_bomb_interval = min(400, self.new_bomb_interval + 2)

    def get_game_parameters(self):
        """Return the current game parameters."""
        return {
            "apple_fall_speed": self.apple_fall_speed,
            "new_apple_interval": self.new_apple_interval,
            "new_bomb_interval": self.new_bomb_interval,
        }
