from ai import create_chess_model, board_to_matrix, mcts_search
import chess
import numpy as np

def self_play(model, num_games=1000):
    """Play self-play games and store training data."""
    training_data = []

    for game_num in range(num_games):
        board = chess.Board()
        move_history = []
        winner = None

        while not board.is_game_over():
            root = Node(board.copy())
            best_move = mcts_search(root, model)
            board.push(best_move)
            move_history.append((board_to_matrix(board), best_move.uci()))

        # Assign rewards based on result
        winner = 1 if board.result() == "1-0" else -1 if board.result() == "0-1" else 0

        for state, move in move_history:
            training_data.append((state, winner))

    return training_data

# Train AI
training_data = self_play(chess_model, num_games=100)
X_train = np.array([state for state, _ in training_data])
y_train = np.array([result for _, result in training_data])

# Train model
chess_model = create_chess_model()
chess_model.fit(X_train, y_train, epochs=20, batch_size=32)
chess_model.save("self_play_chess_model.h5")
