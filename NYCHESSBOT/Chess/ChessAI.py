import chess
import chess.engine
from Chess import ChessEngine

STOCKFISH_PATH = "/opt/homebrew/bin/stockfish"

def findBestMoveStockfish(gs, skill_level=20, time_limit=1.0):
    """
    Use Stockfish at a specified skill level (0–20).
    :param gs: Your custom GameState with a getFEN() method
    :param skill_level: 0 = easiest, 20 = strongest
    :param time_limit: Time in seconds for Stockfish to think
    :return: A ChessEngine.Move instance
    """
    board = chess.Board(gs.getFEN())
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        # Set the engine's skill level
        engine.configure({"Skill Level": skill_level})

        # Let Stockfish pick a move within the given time limit
        result = engine.play(board, limit=chess.engine.Limit(time=time_limit))
        best_move = result.move
        return convertStockfishMoveToCustomMove(gs, best_move)

def convertStockfishMoveToCustomMove(gs, stockfish_move):
    """
    Converts the python-chess Move into your ChessEngine.Move object.
    """
    start_square = stockfish_move.from_square
    end_square = stockfish_move.to_square
    start_row, start_col = divmod(start_square, 8)
    end_row, end_col = divmod(end_square, 8)

    # Flip rows to match your board’s indexing
    start_row = 7 - start_row
    end_row = 7 - end_row

    return ChessEngine.Move((start_row, start_col), (end_row, end_col), gs.board)
