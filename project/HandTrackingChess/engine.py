import chess.engine
from Constants import STOCKFISH_PATH, SCREEN_SIZE, SQUARE_SIZE

class ChessEngine:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def make_move(self, uci_move):
        """
        Makes a move on the board.
        """
        move = chess.Move.from_uci(uci_move)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def get_best_move(self):
        """
        Uses Stockfish to calculate the best move for the current board state.
        """
        result = self.engine.play(self.board, chess.engine.Limit(time=1.0))  # 1 second think time
        return result.move

    def evaluate_board_with_stockfish(self):
        """
        Uses Stockfish to evaluate the board position.
        Returns the evaluation score (positive for white, negative for black).
        """
        info = self.engine.analyse(self.board, chess.engine.Limit(time=0.1))
        score = info["score"]
        if score.is_mate():
            return 1000 if score.mate() > 0 else -1000  # Large positive/negative for mate
        return score.white().score(mate_score=1000) / 100.0  # Normalize to a smaller range

    def get_draw_move(self):
        """
        Finds the move that brings the evaluation as close to 0 as possible.
        """
        best_move = None
        closest_eval = float('inf')

        for move in self.board.legal_moves:
            self.board.push(move)
            eval_score = abs(self.evaluate_board_with_stockfish())  # Absolute value to find the closest to 0
            if eval_score < closest_eval:
                closest_eval = eval_score
                best_move = move
            self.board.pop()

        return best_move

    def handle_bot_turn(self, game_state):
        """
        Handle the bot's turn and return the updated game state.
        """
        move = self.get_draw_move()  # Get the move that keeps evaluation closest to 0
        if move:
            game_state["bot_last_move"] = move  # Track the bot's last move
            self.make_move(move.uci())  # Execute the move
            game_state["evaluation_score"] = self.evaluate_board_with_stockfish()  # Update evaluation
            if self.is_game_over():
                game_state["game_over"] = True  # End the game if it's over
            else:
                game_state["player_turn"] = True  # Switch back to player's turn

        return game_state

    def is_game_over(self):
        """
        Checks if the game is over.
        """
        return self.board.is_game_over()

    def get_game_result(self):
        """
        Returns the result of the game if it's over.
        """
        return self.board.result()

    def close(self):
        """
        Shuts down the Stockfish engine.
        """
        self.engine.quit()
