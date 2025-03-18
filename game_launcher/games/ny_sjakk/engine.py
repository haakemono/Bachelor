import chess
import chess.engine
import os

class ChessEngine:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.turn = "white"

        if not os.path.isfile(stockfish_path):
            raise FileNotFoundError(f"Stockfish not found at {stockfish_path}")

        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def get_valid_moves(self, square):
        return [move.to_square for move in self.board.legal_moves if move.from_square == square]

    def make_move(self, move_uci):
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                if self.board.piece_at(move.from_square).piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
                    if not move.promotion:
                        move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                self.board.push(move)
                self.turn = "black" if self.turn == "white" else "white"
                return True
            return False
        except ValueError:
            return False

    def is_game_over(self):
        return self.board.is_game_over()

    def get_game_result(self):
        return self.board.result() if self.board.is_game_over() else "Game in progress"

    def get_piece_at(self, square):
        return self.board.piece_at(square)

    def ai_move(self, skill_level=5):
        skill_level = max(1, min(10, skill_level))
        self.engine.configure({"Skill Level": skill_level})
        result = self.engine.play(self.board, chess.engine.Limit(depth=skill_level))
        self.board.push(result.move)
        return result.move

    def close(self):
        self.engine.quit()