import cv2
import mediapipe as mp
from collections import deque
import pygame
import chess
from Constants import SCREEN_SIZE, SQUARE_SIZE

#### HOVERING HAND TRACKER
class HandTracker:
    def __init__(self, width, smoothing_window_size=5, frame_skip=2):
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.width = width
        self.smoothing_window_size = smoothing_window_size
        self.frame_skip = frame_skip
        self.frame_count = 0
        self.position_history = deque(maxlen=smoothing_window_size)
        self.hand_landmarks = None
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera.")

    def get_player_position(self):
        self.frame_count += 1

        if self.frame_count % self.frame_skip != 0:
            return None

        ret, frame = self.cap.read()
        if not ret:
            return None

        small_frame = cv2.resize(frame, (320, 240))
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            self.hand_landmarks = results.multi_hand_landmarks[0]

            # Track the index finger tip (Landmark 8)
            index_finger_tip = self.hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            player_x = int((1 - index_finger_tip.x) * self.width)  # Invert x-axis for opposite movement
            player_y = int(index_finger_tip.y * self.width)  # Scale y-coordinate similarly

            # Append the new position to the history
            self.position_history.append((player_x, player_y))

        if self.position_history:
            # Smooth the position using the history
            smoothed_x, smoothed_y = map(
                lambda v: int(sum(v) / len(v)),
                zip(*self.position_history)
            )
            return smoothed_x, smoothed_y

        return None

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        if self.hands is not None:
            self.hands.close()


def handle_player_turn(hand_tracker, engine, game_state):
    """Handle the player's turn, including hand tracking, smoothing, and piece selection."""
    # Get the hand position
    player_position = hand_tracker.get_player_position()
    if player_position:
        game_state["last_hand_position"] = player_position

    # Use the last known position for smoothing
    dot_x, dot_y = game_state["last_hand_position"]
    game_state["smoothed_x"] = int(game_state["alpha"] * dot_x + (1 - game_state["alpha"]) * game_state["smoothed_x"])
    game_state["smoothed_y"] = int(game_state["alpha"] * dot_y + (1 - game_state["alpha"]) * game_state["smoothed_y"])

    # Ensure the dot stays within the chessboard boundaries
    game_state["smoothed_x"] = max(0, min(game_state["smoothed_x"], SCREEN_SIZE - 1))
    game_state["smoothed_y"] = max(0, min(game_state["smoothed_y"], SCREEN_SIZE - 1))

    # Map smoothed dot position to chessboard square
    col = game_state["smoothed_x"] // SQUARE_SIZE
    row = game_state["smoothed_y"] // SQUARE_SIZE
    square = chess.square(col, 7 - row)

    # Hovering logic
    if game_state["hovered_square"] == square:
        if game_state["hover_start_time"] is None:
            game_state["hover_start_time"] = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - game_state["hover_start_time"] >= 2000:
            piece = engine.board.piece_at(square)
            if game_state["selected_square"] is None:
                if piece and piece.color == chess.WHITE:  # Only allow white moves
                    game_state["selected_square"] = square
                    game_state["valid_moves"] = [
                        move.to_square for move in engine.board.legal_moves if move.from_square == square
                    ]
            else:
                if square in game_state["valid_moves"]:
                    move = chess.Move(from_square=game_state["selected_square"], to_square=square)
                    if engine.make_move(move.uci()):
                        game_state["player_turn"] = False  # Switch to bot's turn
                        game_state["evaluation_score"] = engine.evaluate_board_with_stockfish()
                        if engine.is_game_over():
                            game_state["game_over"] = True
                    game_state["selected_square"] = None
                    game_state["valid_moves"] = []
                elif piece and piece.color == chess.WHITE:
                    game_state["selected_square"] = square
                    game_state["valid_moves"] = [
                        move.to_square for move in engine.board.legal_moves if move.from_square == square
                    ]
            game_state["hover_start_time"] = None
    else:
        game_state["hovered_square"] = square
        game_state["hover_start_time"] = pygame.time.get_ticks()

    return game_state
