import pygame
import random

BASKET_WIDTH = 100
BASKET_HEIGHT = 20
APPLE_RADIUS = 15
BOMB_RADIUS = 15

class GameLogic:
    def __init__(self, width, height, font):
        """
        Initializes the game logic.
        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
            font (pygame.font.Font): The font to use for rendering text.
        """
        self.WIDTH = width
        self.HEIGHT = height
        self.FONT = font

    def draw(self, WIN, BG, player, apples, bombs, score, lives, game_over):
        """
        Draws all game elements onto the window.
        Args:
            WIN (pygame.Surface): The game window surface.
            BG (pygame.Surface): The background image surface.
            player (pygame.Rect): The player's basket rectangle.
            apples (list): List of apple positions.
            bombs (list): List of bomb positions.
            score (int): The player's current score.
            lives (int): The player's remaining lives.
            game_over (bool): Whether the game is over.
        """
        WIN.blit(BG, (0, 0))
        pygame.draw.rect(WIN, "brown", player)

        for apple in apples:
            pygame.draw.circle(WIN, "red", (apple[0], apple[1]), APPLE_RADIUS)

        for bomb in bombs:
            pygame.draw.circle(WIN, "blue", (bomb[0], bomb[1]), BOMB_RADIUS)

        if game_over:
            game_over_text = self.FONT.render("GAME OVER", True, "red")
            WIN.blit(game_over_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2 - 20))
            pygame.display.update()
            return

        score_text = self.FONT.render(f"Score: {score}", True, "black")
        lives_text = self.FONT.render(f"Lives: {lives}", True, "black")
        WIN.blit(score_text, (10, 10))
        WIN.blit(lives_text, (10, 40))
        pygame.display.update()

    def reset_game(self):
        """
        Resets the game state.
        Returns:
            dict: The initial game state.
        """
        return {
            "player": pygame.Rect(200, self.HEIGHT - BASKET_HEIGHT, BASKET_WIDTH, BASKET_HEIGHT),
            "apples": [],
            "bombs": [],
            "score": 0,
            "lives": 3,
            "frame_count": 0,
            "game_over": False,
        }

    def update_objects(self, apples, bombs, apple_fall_speed):
        """
        Updates the positions of apples and bombs.
        Args:
            apples (list): List of apple positions.
            bombs (list): List of bomb positions.
            apple_fall_speed (float): The speed at which apples fall.
        """
        for apple in apples:
            apple[1] += apple_fall_speed
        for bomb in bombs:
            bomb[1] += 4

        # Remove off-screen objects
        apples[:] = [a for a in apples if a[1] < self.HEIGHT]
        bombs[:] = [b for b in bombs if b[1] < self.HEIGHT]

    def spawn_object(self, objects, radius):
        """
        Spawns a new object (apple or bomb) at a random position.
        Args:
            objects (list): List to append the new object to.
            radius (int): The radius of the object.
        """
        x_pos = random.randint(radius, self.WIDTH - radius)
        objects.append([x_pos, 0])

    def check_collision(self, obj_x, obj_y, player_x, player_y, radius):
        """
        Checks if an object collides with the player's basket.
        Args:
            obj_x (int): The x-coordinate of the object.
            obj_y (int): The y-coordinate of the object.
            player_x (int): The x-coordinate of the player's basket.
            player_y (int): The y-coordinate of the player's basket.
            radius (int): The radius of the object.
        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        return (
            player_x < obj_x < player_x + BASKET_WIDTH
            and player_y < obj_y + radius < player_y + BASKET_HEIGHT
        )

    def handle_collisions(self, objects, game_state, difficulty_manager, is_apple=True):
        """
        Handles collisions between objects (apples or bombs) and the player's basket.
        Args:
            objects (list): List of object positions.
            game_state (dict): The current game state.
            difficulty_manager (DifficultyManager): The difficulty manager instance.
            is_apple (bool): Whether the objects are apples (True) or bombs (False).
        """
        for obj in objects[:]:
            if self.check_collision(
                obj[0], obj[1],
                game_state["player"].x, game_state["player"].y,
                APPLE_RADIUS if is_apple else BOMB_RADIUS
            ):
                if is_apple:
                    game_state["score"] += 1
                    reaction_time = game_state["frame_count"] / 60  # Reaction time in seconds
                    difficulty_manager.track_performance(caught=True, reaction_time=reaction_time)
                else:
                    game_state["lives"] -= 1
                    if game_state["lives"] <= 0:
                        game_state["game_over"] = True
                objects.remove(obj)