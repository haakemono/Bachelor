import tensorflow as tf
import numpy as np
import chess
import math
import random

# Neural Network Model
INPUT_SHAPE = (8, 8, 12)

def create_chess_model():
    """Creates a CNN model for chess move evaluation."""
    inputs = tf.keras.layers.Input(shape=INPUT_SHAPE)

    x = tf.keras.layers.Conv2D(64, (3, 3), activation='relu', padding='same')(inputs)
    x = tf.keras.layers.Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.Flatten()(x)

    # Policy Head
    policy = tf.keras.layers.Dense(512, activation='relu')(x)
    policy = tf.keras.layers.Dense(64, activation='softmax', name="policy")(policy)

    # Value Head
    value = tf.keras.layers.Dense(256, activation='relu')(x)
    value = tf.keras.layers.Dense(1, activation='tanh', name="value")(value)

    model = tf.keras.models.Model(inputs=inputs, outputs=[policy, value])
    model.compile(optimizer='adam', loss=['categorical_crossentropy', 'mse'])

    return model

# Convert board to AI-compatible format
def board_to_matrix(board):
    """Converts chess board to a 8x8x12 matrix for AI input."""
    piece_map = {
        'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
        'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
    }
    board_matrix = np.zeros((8, 8, 12))

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = divmod(square, 8)
            board_matrix[row][col][piece_map[piece.symbol()]] = 1

    return board_matrix

# MCTS Node
class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def uct_score(self, exploration_weight=1.4):
        """Calculate UCT score for exploration vs exploitation."""
        if self.visits == 0:
            return float('inf')
        return self.value / self.visits + exploration_weight * math.sqrt(math.log(self.parent.visits) / self.visits)

# Monte Carlo Tree Search (MCTS)
def mcts_search(root, model, simulations=50):
    for _ in range(simulations):
        node = root
        board_copy = root.board.copy()

        # Selection & Expansion
        while node.children:
            node = max(node.children, key=lambda n: n.uct_score())
            board_copy.push(node.move)

        # Simulation (Predict outcome using neural network)
        board_matrix = board_to_matrix(board_copy)
        policy, value = model.predict(np.array([board_matrix]))

        # Expand with legal moves
        legal_moves = list(board_copy.legal_moves)
        node.children = [Node(board_copy.copy(), move=m, parent=node) for m in legal_moves]

        # Backpropagation
        reward = value[0][0]
        while node:
            node.visits += 1
            node.value += reward
            reward = -reward
            node = node.parent

    best_child = max(root.children, key=lambda n: n.visits)
    return best_child.move

