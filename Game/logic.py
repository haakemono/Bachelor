import pygame
import random
from constants import WIDTH, HEIGHT, BASKET_HEIGHT, BASKET_WIDTH

def reset_game():
    """Reset the game state to its initial values."""
    return {
        "player": pygame.Rect(200, HEIGHT - BASKET_HEIGHT, BASKET_WIDTH, BASKET_HEIGHT),
        "apples": [],
        "bombs": [],
        "score": 0,
        "true_score": 0,  # Add true score to track total apples spawned
        "lives": 3,
        "frame_count": 0,
        "game_over": False,
    }

def spawn_object(objects, radius, game_state=None):
    """Spawn an object (apple or bomb) at a random position."""
    x = random.randint(radius, WIDTH - radius)
    y = 0
    objects.append({"x": x, "y": y, "radius": radius})

    # Increment true score for apples
    if game_state and objects == game_state["apples"]:
        game_state["true_score"] += 1

def update_objects(objects, fall_speed, game_state=None):
    """Update the position of objects and remove those that fall off the screen."""
    updated_objects = []
    for obj in objects:
        obj["y"] += fall_speed
        if obj["y"] + obj["radius"] < HEIGHT:
            updated_objects.append(obj)  # Keep objects still on screen
        elif game_state and objects == game_state["apples"]:
            # Increment true_score if the apple is missed (falls off screen)
            game_state["true_score"] += 1
    objects[:] = updated_objects


def handle_collisions(objects, player, game_state, score_increment=1, life_decrement=1):
    """Handle collisions between objects and the player."""
    collided = []
    for obj in objects:
        obj_rect = pygame.Rect(obj["x"] - obj["radius"], obj["y"] - obj["radius"], obj["radius"] * 2, obj["radius"] * 2)
        if player.colliderect(obj_rect):  # Ensure player is a pygame.Rect
            if score_increment:
                game_state["score"] += score_increment
            if life_decrement:
                game_state["lives"] -= life_decrement
                if game_state["lives"] <= 0:
                    game_state["game_over"] = True
            if objects == game_state["apples"]:
                # Increment true_score when apple is caught
                game_state["true_score"] += 1
            collided.append(obj)
    for obj in collided:
        objects.remove(obj)

