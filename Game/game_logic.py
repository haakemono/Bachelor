import pygame
import random


class GameLogic:
    def __init__(self, width, height, font):
        self.WIDTH = width
        self.HEIGHT = height
        self.FONT = font

    def draw(self, WIN, BG, player, apples, bombs, score, lives, game_over):
        WIN.blit(BG, (0, 0))
        pygame.draw.rect(WIN, "brown", player)

        for apple in apples:
            pygame.draw.circle(WIN, "red", (apple[0], apple[1]), 15)

        for bomb in bombs:
            pygame.draw.circle(WIN, "blue", (bomb[0], bomb[1]), 15)

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
        return {
            "player": pygame.Rect(200, self.HEIGHT - 20, 100, 20),
            "apples": [],
            "bombs": [],
            "score": 0,
            "lives": 3,
            "frame_count": 0,
            "game_over": False,
        }

    def update_objects(self, apples, bombs, apple_fall_speed):
        # Move apples and bombs
        for apple in apples:
            apple[1] += apple_fall_speed
        for bomb in bombs:
            bomb[1] += 4

        # Remove off-screen objects
        apples[:] = [a for a in apples if a[1] < self.HEIGHT]
        bombs[:] = [b for b in bombs if b[1] < self.HEIGHT]

    def spawn_apple(self, apples):
        apple_x = random.randint(15, self.WIDTH - 15)
        apples.append([apple_x, 0])

    def spawn_bomb(self, bombs):
        bomb_x = random.randint(15, self.WIDTH - 15)
        bombs.append([bomb_x, 0])

    def check_collisions(self, game_state, difficulty_manager):
        # Check apple collisions
        for apple in game_state["apples"][:]:
            if (
                game_state["player"].x < apple[0] < game_state["player"].x + 100
                and game_state["player"].y < apple[1] + 15 < game_state["player"].y + 20
            ):
                game_state["score"] += 1
                game_state["apples"].remove(apple)
                reaction_time = game_state["frame_count"] / 60  # Reaction time in seconds
                difficulty_manager.track_performance(caught=True, reaction_time=reaction_time)

        # Check bomb collisions
        for bomb in game_state["bombs"][:]:
            if (
                game_state["player"].x < bomb[0] < game_state["player"].x + 100
                and game_state["player"].y < bomb[1] + 15 < game_state["player"].y + 20
            ):
                game_state["lives"] -= 1
                game_state["bombs"].remove(bomb)
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True
