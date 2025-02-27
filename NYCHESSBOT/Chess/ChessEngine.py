class GameState():
    def __init__(self):
        self.board = [
            ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
        ]

        self.moveFunctions = {'p': self.getPawnMoves, 'r': self.getRookMoves, 'n': self.getKnightMoves,
                              'b': self.getBishopMoves, 'q': self.getQueenMoves, 'k': self.getKingMoves}

        self.moveLog = []
        self.whiteToMove = True
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible = ()
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(True, True, True, True)]

    def makeMove(self, move):
        """Executes a move on the board."""
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # Switch player turns

        # Update king location if moved
        if move.pieceMoved == 'wk':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bk':
            self.blackKingLocation = (move.endRow, move.endCol)

        # Pawn promotion (auto-promote to queen)
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'q'

        # En passant move
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"

        # Handle castling
        if move.castle:
            if move.endCol - move.startCol == 2:  # Kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:  # Queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        # Update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,
                                                 self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs,
                                                 self.currentCastlingRight.bqs))

    def undoMove(self):
        """Undoes the last move."""
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back

            # Restore king positions
            if move.pieceMoved == 'wk':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)

            self.checkmate = False
            self.stalemate = False

    def getValidMoves(self):
        """Returns all legal moves."""
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        """Generates all legal moves for the current player."""
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece == "--":
                    continue

                turn = piece[0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    pieceType = piece[1]
                    if pieceType in self.moveFunctions:
                        self.moveFunctions[pieceType](r, c, moves)

        return moves

    def getPawnMoves(self, r, c, moves):
        """Handles pawn movement."""
        direction = 1 if self.whiteToMove else -1
        startRow = 6 if self.whiteToMove else 1  # White pawns start at row 6, black at row 1
        if self.board[r + direction][c] == "--":  # Move forward
            moves.append(Move((r, c), (r + direction, c), self.board))
            if r == startRow and self.board[r + 2 * direction][c] == "--":  # Double move
                moves.append(Move((r, c), (r + 2 * direction, c), self.board))

        # Capture diagonally
        if c - 1 >= 0 and self.board[r + direction][c - 1][0] == ('b' if self.whiteToMove else 'w'):
            moves.append(Move((r, c), (r + direction, c - 1), self.board))
        if c + 1 <= 7 and self.board[r + direction][c + 1][0] == ('b' if self.whiteToMove else 'w'):
            moves.append(Move((r, c), (r + direction, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        """Handles rook movement."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            row, col = r, c
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self.board))
                    elif self.board[row][col][0] != ('b' if self.whiteToMove else 'w'):
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        """Handles knight movement."""
        knightMoves = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        for move in knightMoves:
            row, col = r + move[0], c + move[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] == "--" or self.board[row][col][0] != ('b' if self.whiteToMove else 'w'):
                    moves.append(Move((r, c), (row, col), self.board))

    def getBishopMoves(self, r, c, moves):
        """Handles bishop movement."""
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for direction in directions:
            row, col = r, c
            while True:
                row += direction[0]
                col += direction[1]
                if 0 <= row < 8 and 0 <= col < 8:
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self.board))
                    elif self.board[row][col][0] != ('b' if self.whiteToMove else 'w'):
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        """Handles queen movement."""
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        """Handles king movement."""
        kingMoves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for move in kingMoves:
            row, col = r + move[0], c + move[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] == "--" or self.board[row][col][0] != ('b' if self.whiteToMove else 'w'):
                    moves.append(Move((r, c), (row, col), self.board))

    def updateCastleRights(self, move):
        """Update the castle rights after each move."""
        if move.pieceMoved == 'wk':
            self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bk':
            self.currentCastlingRight.bks = False
        elif move.pieceMoved == 'wr' and move.startRow == 7:
            if move.startCol == 0:
                self.currentCastlingRight.wqs = False
            elif move.startCol == 7:
                self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'br' and move.startRow == 0:
            if move.startCol == 0:
                self.currentCastlingRight.bqs = False
            elif move.startCol == 7:
                self.currentCastlingRight.bks = False


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    """Represents a chess move."""
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant=False, castle=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.pawnPromotion = self.pieceMoved[1] == 'p' and (self.endRow == 0 or self.endRow == 7)
        self.castle = castle
        self.enPassant = enPassant

    def __eq__(self, other):
        return isinstance(other, Move) and self.startRow == other.startRow and self.startCol == other.startCol and \
               self.endRow == other.endRow and self.endCol == other.endCol

    def getChessNotation(self):
        return self.colsToFiles[self.startCol] + self.rowsToRanks[self.startRow] + self.colsToFiles[self.endCol] + self.rowsToRanks[self.endRow]
