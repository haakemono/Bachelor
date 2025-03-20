import pygame as p
from Chess import ChessEngine, ChessAI
from multiprocessing import Process, Queue

# Constants
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_WIDTH_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

# Load Images
def loadImages():
    pieces = ['wp', 'wr', 'wn', 'wb', 'wk', 'wq', 'bp', 'br', 'bn', 'bb', 'bk', 'bq']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/assets/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# Main Game Loop
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH +  MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial",12,False,False)
    gs = ChessEngine.GameState()
    print("Getting valid moves...")
    validMoves = gs.getValidMoves()
    print("Valid moves found:", validMoves)
    moveMade = False
    animate = False 
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    playerOne = True  # if human is playing white this will be true
    playerTwo = False# same as above but for black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE

                    if sqSelected == (row, col) or col >= 8:  # Clicked same square -> Deselect
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)  # Append click

                    if len(playerClicks) == 2 and humanTurn:  # Only try move when two squares are clicked
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)

                        for validMove in validMoves:
                            if move.startRow == validMove.startRow and move.startCol == validMove.startCol and \
                            move.endRow == validMove.endRow and move.endCol == validMove.endCol:
                                gs.makeMove(validMove)
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                                break  # Stop checking once a valid move is found

                        if not moveMade:
                            playerClicks = [sqSelected]  # Reset clicks if move is invalid

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # Undo last move
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                        moveUndone = True

                if e.key == p.K_r:  # Restart the game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()  # Ensure valid moves are updated
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True

        # AI MOVE FINDER
        # AI MOVE FINDER
        if not gameOver and not humanTurn and not moveUndone:
            if gs.checkmate or gs.stalemate:
                gameOver = True
                drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Checkmate!')
                continue  # Stop processing further moves

            if not AIThinking:
                AIThinking = True
                print("Stockfish thinking...")

                # ENDRE på SKILLLEVEL PÅ BOT
                AIMove = ChessAI.findBestMoveStockfish(gs, skill_level=20, time_limit=1.0)



                if AIMove is None:
                    if gs.checkmate or gs.stalemate:
                        return
                    else:
                        AIMove = ChessAI.findRandomMoves(validMoves)

                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking = False


# Move animations and valid move updates
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)

            validMoves = gs.getValidMoves()  # ✅ Ensure valid moves are updated
            moveMade = False
            animate = False
            moveUndone = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or gs.stalemate:
            gameOver = True
            drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')

        clock.tick(MAX_FPS)
        p.display.flip()

        
# Highlight the square selected and moves for the piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):  # Only highlight the right pieces
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # Transparency
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            # Highlight possible moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))

# Draw Game State
def drawGameState(screen, gs, validMoves, sqSelected,moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen,gs,moveLogFont)

# Draw Chess Board
def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Draw Chess Pieces
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH,0,MOVE_LOG_PANEL_WIDTH,MOVE_LOG_PANEL_WIDTH_HEIGHT)
    p.draw.rect(screen, p.Color("black"),moveLogRect)
    moveLog = gs.moveLog
    moveText = []
    for i in range(0,len(moveLog),2):
        moveString = str(i//2 +1) + '. ' + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) +"   "
        moveText.append(moveString)
    movesPerRow = 3
    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveText), movesPerRow):
        text = ""
        for j in range(movesPerRow): 
            if i + j < len(moveText):
                text += moveText[i+j]
                
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding,textY)
        screen.blit(textObject,textLocation)
        textY += textObject.get_height() + lineSpacing

# Animate moves
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            if move.enPassant:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else move.endRow -1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enPassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        if move.pieceMoved != '--':
            screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

# Display endgame text
def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textObject.get_width() / 2, BOARD_HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))

if __name__ == "__main__":
    main()
