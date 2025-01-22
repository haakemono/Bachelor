import chess

class ChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.turn = "white"

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
                if self.board.piece_at(move.from_square).piece_type == chess.PAWN:
                    if chess.square_rank(move.to_square) in [0, 7]:  # Promotion rank
                        move.promotion = chess.QUEEN  # Default to queen promotion
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
