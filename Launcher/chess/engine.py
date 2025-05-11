import chess
import chess.engine
import os

"""
Sets up the chess engine and board, and starts Stockfish from the given path
"""
class ChessEngine:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.turn = "white"

        if not os.path.isfile(stockfish_path):
            raise FileNotFoundError(f"Stockfish not found at {stockfish_path}")

        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
    
    """
    Returns a list of legal destinations square for the piece on the given square.
    """
    def get_valid_moves(self, square):
        return [move.to_square for move in self.board.legal_moves if move.from_square == square]

    
    """
    Tries to apply a move in UCI format to the board.
    Automatically promotes pawn to queen if they reach the last rank
    Returns True if the moves is legal and applied, False otherwise
    """
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

    """
    check if the game has ended(stalemate, checkmate etc.)
    Return the final game result if the game is over, or says "Games in progress"
    Returns the piece currently on the specified square 
    """
    def is_game_over(self):
        return self.board.is_game_over()

    def get_game_result(self):
        return self.board.result() if self.board.is_game_over() else "Game in progress"

    def get_piece_at(self, square):
        return self.board.piece_at(square)

    """#
    Asks stockfish to compute the best moved based on the current board state and selected skill level (1-10).
    Returns the move without applying it.
    Then shuts down the stockfish engine cleanly to free up resources.
    """
    def ai_move(self, skill_level=5):
        skill_level = max(1, min(10, skill_level))
        stockfish_skill = (skill_level - 1) * 2

        self.engine.configure({
            "Skill Level": stockfish_skill
        })

        result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
        return result.move  # Do not push yet — push after animation in main()

    def close(self):
        self.engine.quit()