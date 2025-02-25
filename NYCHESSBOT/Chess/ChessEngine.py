
class GameState():
    def __init__(self):
        self.board = [
            ['br','bn','bb','bq','bk','bb','bn','br'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wr','wn','wb','wq','wk','wb','wn','wr']]

        self.moveFunctions = {'p':self.getPawnMoves,'r': self.getRookMoves, 'n': self.getKnightMoves,
                              'b': self.getBishopMoves, 'q': self.getQueenMoves,'k':self.getKingMoves}

        self.moveLog = []
        self.whiteToMove = True
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck= False
        self.checks = []
        self.pins = []
        self.checkmate = False 
        self.stalemate = False     
        self.enPassantPossible = ()
        self.enPassantPossibleLog = [self.enPassantPossible]
        
        self.currentCastlingRight = CastleRights(True,True,True,True)
        self.castleRightsLog= [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

        

    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)  # Log move
        self.whiteToMove = not self.whiteToMove  # Switch turns

        # 🏁 Update King's position if moved
        if move.pieceMoved == 'wk':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bk':
            self.blackKingLocation = (move.endRow, move.endCol)
            
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow)//2, move.endCol)

        # 🏁 Handle En Passant
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        
        # 🏁 Handle Pawn Promotion
        if move.pawnPromotion:
            #promoted piece = input("promote to "Q", "R", "B" or "N")
            promotedPiece = 'q'  # You can later allow users to choose this
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotedPiece

        # 🏁 Handle Castling
        if move.castle:
            if move.endCol - move.startCol == 2:  # Kingside
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # Move rook
                self.board[move.endRow][move.endCol + 1] = '--'
            else:  # Queenside
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # Move rook
                self.board[move.endRow][move.endCol - 2] = '--'

        # 🏁 Update En Passant Availability
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.startRow + move.endRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()

        self.enPassantPossibleLog.append(self.enPassantPossible)
  


            
        #update castling right -whenever it is a rook or a king move
        
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))
 
        

            
            
    
    def undoMove(self):
        if len(self.moveLog) != 0:  # Make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Switch turns back
            
            # Update the king's position if needed
            if move.pieceMoved == 'wk':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bk':
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                
            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]


            #undo the castling rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            # get rid of the castle rights from the move we are undoing
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            #castle move
            if move.castle:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:  # queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
                    
            self.checkmate = False
            self.stalemate = False

        
        #update the castle rights given the move
                
    def updateCastleRights(self, move): 
        if move.pieceMoved == 'wk' :
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bk' :
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wr' :
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                   self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'br' :
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                   self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False 
        
    
        



    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
        else:
            kingRow, kingCol = self.blackKingLocation

        if self.inCheck:
            if len(self.checks) == 1:  # Single check -> must block or move king
                moves = self.getAllPossibleMoves()
                check = self.checks[0]  # Get attacking piece
                checkRow, checkCol = check[0], check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []

                if pieceChecking[1] == 'n':  # Knights must be captured
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        square = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(square)
                        if square == (checkRow, checkCol):
                            break

                # Remove moves that don't block check or move the king
                moves = [move for move in moves if (move.endRow, move.endCol) in validSquares]
            
            else:  # Double check -> king must move
                self.getKingMoves(kingRow, kingCol, moves)
        
        else:  # Not in check, generate all moves
            moves = self.getAllPossibleMoves()
        
        # **Checkmate & Stalemate Handling**
        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

            
    
            
        
    


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                piece = self.board[r][c]
                if piece == "--":  # Skip empty squares
                    continue

                turn = piece[0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    pieceType = piece[1]
                    if pieceType in self.moveFunctions:  # Ensure move function exists
                        self.moveFunctions[pieceType](r, c, moves)
        
        return moves


        
    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            enemyColor = 'b'
            kingRow, KingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            enemyColor = 'w'
            kingRow, KingCol = self.blackKingLocation


        if self.board[r+moveAmount][c] == "--":  # 1 square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                moves.append(Move((r, c), (r+moveAmount, c), self.board))
                if r == startRow and self.board[r+2*moveAmount][c] == "--":  # 2 square moves
                    moves.append(Move((r, c), (r+2*moveAmount, c), self.board))
        if c-1 >= 0:  # Capture to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board))
                if (r + moveAmount, c - 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if KingCol < c:
                            insideRange = range(KingCol +1,c-1)
                            outsideRange = range(c+1, 8)
                        else:
                            insideRange = range(KingCol-1,c,-1)
                            outsideRange = range(c-2,-1,-1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "r" or square[1] == 'q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece=True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant=True))

        if c+1 <= 7:  # Capture to right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board))
                if (r + moveAmount, c + 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if KingCol < c:
                            insideRange = range(KingCol +1,c)
                            outsideRange = range(c+2, 8)
                        else:
                            insideRange = range(KingCol-1,c+1,-1)
                            outsideRange = range(c-1,-1,-1)
                        for i in insideRange:
                            if self.board[r][i] != "--":
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "r" or square[1] == 'q'):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece=True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant=True))
                        

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                break  # ✅ Do NOT remove the pin entry

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Rook moves in straight lines
        enemyColor = "b" if self.whiteToMove else "w"

        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # ✅ Stay within board
                    if not piecePinned or pinDirection in [d, (-d[0], -d[1])]:  # ✅ Pinned pieces must move in pin direction
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # ✅ Empty space
                            move = Move((r, c), (endRow, endCol), self.board)
                            moves.append(move)
                        elif endPiece[0] == enemyColor:  # ✅ Capture enemy piece
                            move = Move((r, c), (endRow, endCol), self.board)
                            moves.append(move)
                            break  # ✅ Stop after capturing
                        else:
                            break  # ✅ Stop if blocked by a friendly piece
                else:
                    break  # ✅ Stop if off board




    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece)
                        moves.append(Move((r, c), (endRow, endCol), self.board))




    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # Diagonal directions
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # On board
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # Empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # Enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # Friendly piece invalid
                            break
                else:  # Off board
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)




                
    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = "w" if self.whiteToMove else "b"

        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # Not an ally piece (empty or enemy piece)
                    # Place king on end square and check for checks
                    if allyColor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))

                    # Place king back on original location
                    if allyColor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)

        self.getCastleMoves(r, c, moves, allyColor)

                          

    
    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.squareUnderAttack(r, c, allyColor)
        if inCheck:
            return  # Can't castle in check

        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves, allyColor)

        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves, allyColor)


    def getKingsideCastleMoves(self, r, c, moves, allyColor):
    # Check if two squares between king and rook are clear and not under attack
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--' and \
        not self.squareUnderAttack(r, c+1, allyColor) and not self.squareUnderAttack(r, c+2, allyColor):
            moves.append(Move((r, c), (r, c+2), self.board, castle=True))



    def getQueensideCastleMoves(self, r, c, moves, allyColor):

        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' and \
        not self.squareUnderAttack(r, c-1, allyColor) and not self.squareUnderAttack(r, c-2, allyColor):
            moves.append(Move((r, c), (r, c-2), self.board, castle=True))


                            
                        
    def checkForPinsAndChecks(self):
        pins = [] # squares where the allied pinned piece is and direction pinned from
        checks = [] # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # Reset possible pins
            
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    
                    if endPiece[0] == allyColor and endPiece[1] != 'k':  # ✅ Make sure pinned pieces are handled correctly
                        if possiblePin == ():  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])

                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king (this is necessary to prevent a king move to a square controlled by another king)
                        if (0 <= j <= 3 and type == 'r') or \
                                (4 <= j <= 7 and type == 'b') or \
                                (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'q') or (i == 1 and type == 'k'):
                            if possiblePin == ():  # no piece blocking, so check
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break # off board

        # check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'n':  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck, pins, checks
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wk':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bk':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wr':
            if move.startRow == 7:
                if move.startCol == 0:  # Left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:  # Right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'br':
            if move.startRow == 0:
                if move.startCol == 0:  # Left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False
                    
        #if a rook is captured
        if move.pieceCaptured == 'wr':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'br ':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


        
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])

        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    def squareUnderAttack(self, r, c, allyColor):
        enemyColor = 'w' if allyColor == 'b' else 'b'
        directions = directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)) 

        for j in range(len(directions)):
            d = directions[j]
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:  # No attack from that direction
                        break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in this complex conditional
                        # 1.) Orthogonally away from square and piece is a rook
                        # 2.) Diagonally away from square and piece is a bishop
                        # 3.) 1 square away diagonally from square and piece is a pawn
                        # 4.) Any direction and piece is a queen
                        # 5.) Any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and type == 'r') or \
                                (4 <= j <= 7 and type == 'b') or \
                                (i == 1 and type == 'p' and (
                                        (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'q') or (i == 1 and type == 'k'):
                            return True
                        else:  # enemy piece not applying check
                            break
                    else:
                        break  # off board

        # Check for knight checks
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]

            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'n':
                    return True
        return False
    
        
    def checkmate(self):
        return self.checkmate

    def stalemate(self):
        return self.stalemate

    
class CastleRights():
    def __init__(self, wks, bks,wqs,bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
        self.castleRightsLog = []  



                
    
class Move():
    # maps keys to values
# key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, 
                "5": 3, "6": 2, "7": 1, "8": 0}

    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
                "e": 4, "f": 5, "g": 6, "h": 7}

    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant = False, castle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.pawnPromotion = self.pieceMoved[1] == 'p' and (self.endRow == 0 or self.endRow == 7)
        self.castle = castle
        self.enPassant = enPassant
        if enPassant:
            self.pieceCaptured = 'bp' if self.pieceMoved == 'wp' else 'wp'
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 +self.endRow * 10 + self.endCol


        

        
            
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def __str__(self):
        if self.castle:
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow,self.endCol)
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" +endSquare
            
            else:
                return endSquare
        
        
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare

            
    
        



