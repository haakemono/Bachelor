import chess
import chess.engine
import os

class ChessEngine:
    def __init__(self, stockfish_path):
        self.board = chess.Board()
        self.turn = "white"

        # Ensure the Stockfish executable exists
        if not os.path.isfile(stockfish_path):
            print(f"Error: Stockfish executable not found at {stockfish_path}")
            raise FileNotFoundError(f"Stockfish not found at {stockfish_path}")
        
        # Initialize Stockfish engine
        self.engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    def display_board(self):
        """
        Print the current board state to the console.
        """
        print(self.board)

    def get_valid_moves(self, square):
        """
        Get a list of all valid moves for a specific square.

        Args:
            square (int): The square index (0-63) to get valid moves for.

        Returns:
            list: A list of target squares (int) that the piece on the given square can move to.
        """
        return [move.to_square for move in self.board.legal_moves if move.from_square == square]

    def make_move(self, move_uci):
        """
        Execute a move if it is valid, handling pawn promotion.

        Args:
            move_uci (str): The move in UCI format (e.g., 'e7e8q').

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                # Check for pawn promotion
                if self.board.piece_at(move.from_square).piece_type == chess.PAWN and chess.square_rank(move.to_square) in [0, 7]:
                    if not move.promotion:
                        # Automatically add queen promotion if not specified
                        move = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                self.board.push(move)
                self.turn = "black" if self.turn == "white" else "white"
                return True
            else:
                print(f"Illegal move: {move_uci}")
                return False
        except ValueError:
            print(f"Invalid move format: {move_uci}")
            return False

    def is_game_over(self):
        """
        Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.board.is_game_over()

    def get_game_result(self):
        """
        Get the result of the game if it is over.

        Returns:
            str: The result of the game ('1-0', '0-1', '1/2-1/2', or 'Game in progress').
        """
        if self.board.is_game_over():
            return self.board.result()
        return "Game in progress"

    def get_piece_at(self, square):
        """
        Get the piece at a specific square.

        Args:
            square (int): The square index (0-63).

        Returns:
            chess.Piece or None: The piece on the given square, or None if empty.
        """
        return self.board.piece_at(square)

    def ai_move(self, difficulty="easy"):
        """
        Let Stockfish make a move after thinking for a specified duration or depth.
        
        Args:
            difficulty (str): The difficulty level of the AI (easy, medium, or hard).
        
        Returns:
            chess.Move: The AI's best move.
        """
        # Define depths based on difficulty
        if difficulty == "easy":
            depth = 1  # Easy = shallow search
        elif difficulty == "medium":
            depth = 3  # Medium = deeper search
        elif difficulty == "hard":
            depth = 5  # Hard = very deep search
        else:
            depth = 3  # Default to medium if an unknown difficulty is provided

        # Use Stockfish to get the best move for the current board
        result = self.engine.play(self.board, chess.engine.Limit(depth=depth))
        self.board.push(result.move)  # Execute the move on the board
        return result.move

    def close(self):
        """Close the engine when done."""
        self.engine.quit()