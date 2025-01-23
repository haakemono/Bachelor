import chess.engine
stockfish_path = r"C:\Users\haako\Downloads\stockfish-windows-x86-64\stockfish\stockfish-windows-x86-64.exe"

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
