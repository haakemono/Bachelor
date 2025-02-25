import random
import multiprocessing
import time

pieceScore = {"k": 0, "q": 9, "r": 5, "b": 3.25, "n": 3, "p": 1}

knightScores = [
    [1, 2, 3, 3, 3, 3, 2, 1],
    [2, 4, 6, 6, 6, 6, 4, 2],
    [3, 6, 8, 9, 9, 8, 6, 3],
    [3, 6, 9, 10, 10, 9, 6, 3],
    [3, 6, 9, 10, 10, 9, 6, 3],
    [3, 6, 8, 9, 9, 8, 6, 3],
    [2, 4, 6, 6, 6, 6, 4, 2],
    [1, 2, 3, 3, 3, 3, 2, 1]
]
bishopScores = [[3 + i for i in range(8)] for _ in range(8)]
rookScores = [[5] * 8 for _ in range(8)]
queenScores = [[9] * 8 for _ in range(8)]
whitePawnScores = [
    [10, 10, 10, 10, 10, 10, 10, 10],
    [8, 9, 9, 9, 9, 9, 9, 8],
    [6, 7, 7, 8, 8, 7, 7, 6],
    [4, 5, 5, 6, 6, 5, 5, 4],
    [3, 4, 4, 5, 5, 4, 4, 3],
    [2, 3, 3, 4, 4, 3, 3, 2],
    [1, 2, 2, 3, 3, 2, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
blackPawnScores = whitePawnScores[::-1]  # Flip for Black

piecePositionScores = {
    "n": knightScores,
    "b": bishopScores,
    "r": rookScores,
    "q": queenScores,
    "wp": whitePawnScores,
    "bp": blackPawnScores
}

CHECKMATE = 100000  # Increased value for accuracy
STALEMATE = 0
DEPTH = 5  # Set deep search depth

# Transposition Table (Caching for faster lookup)
transposition_table = {}

def findBestMove(gs, validMoves, returnQueue):
    """ AI move finder using iterative deepening with Alpha-Beta pruning """
    global nextMove
    start_time = time.time()
    nextMove = None
    moveOrdering(validMoves, gs)  # Order moves before search

    for depth in range(1, DEPTH + 1):  # Iterative deepening
        score = findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
        if time.time() - start_time > 2.0:  # Time control (limit search time)
            break

    # If no best move found, pick a **random move**
    if nextMove is None:
        nextMove = findRandomMove(validMoves)

    returnQueue.put(nextMove)

def moveOrdering(moves, gs):
    """ Orders moves based on material gain for faster pruning """
    moves.sort(key=lambda move: (pieceScore.get(move.pieceCaptured[1], 0)), reverse=True)

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    """ Optimized AI search using Negamax with Alpha-Beta pruning + Transposition Table """
    global nextMove
    boardHash = hash(str(gs.board))  # Create a unique hash for board state

    if boardHash in transposition_table:
        return transposition_table[boardHash]  # Retrieve cached score

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    bestMoves = []
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        gs.undoMove()

        if score > maxScore:
            maxScore = score
            bestMoves = [move]  # Store best move(s)
            if depth == DEPTH:
                nextMove = move

        elif score == maxScore:
            bestMoves.append(move)

        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break  # Alpha-beta cutoff

    transposition_table[boardHash] = maxScore  # Store result in table

    # If multiple best moves, pick one randomly
    if depth == DEPTH and bestMoves:
        nextMove = random.choice(bestMoves)

    return maxScore

def findRandomMove(validMoves):
    """ Picks and returns a random move """
    return validMoves[random.randint(0, len(validMoves) - 1)] if validMoves else None

def scoreBoard(gs):
    """ Evaluates the board position considering material, piece activity, and king safety """
    if gs.checkmate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(8):
        for col in range(8):
            piece = gs.board[row][col]
            if piece != "--":
                pieceType = piece[1]
                piecePositionScore = 0  
                if pieceType != "k":  # No positional scoring for king
                    piecePositionScore = piecePositionScores.get(piece, [[0]*8]*8)[row][col]

                if piece[0] == 'w':
                    score += pieceScore[pieceType] + piecePositionScore * 0.1
                else:
                    score -= pieceScore[pieceType] + piecePositionScore * 0.1
    return score