import pygame
import chess
import chessApp
import sys
import os
import AI
import random

pygame.init()

# NEEDS TO RUN IN 7:5 ASPECT RATIO 1050x750 for 1080p screens, recommended to run at 1400x750
WIDTH = 1050
HEIGHT = 750
LIGHTSQUARE = (151, 226, 196)
DARKSQUARE= (47,131,97)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load(os.path.join('images', 'chessboard.png')))
font = pygame.font.SysFont('Arial_Bold', round((HEIGHT/1000)*30))
big_font = pygame.font.SysFont('Arial_Bold', round((HEIGHT/1000)*50))
timer = pygame.time.Clock()
fps = 60
coords = [] # list for coordinates of any current target squares
legalMovesForSquare = []
targetSquares = []

moveList = [] # move list in short algebraic notation for displaying moves on side menu
fenList = [] # list of FEN strings for each move made on the board, used for implementing back and forward buttons by keeping track of all board postions that have occured in game


currentBestMove = [] # list containing one string representing the current best move in uci notation. list needed for clear() function

playername = "Jaysen"
player2name = "Stockfish"

DEFAULT_IMAGE_SIZE = (round(WIDTH/14), round(HEIGHT/10))
DEFAULT_SMALL_IMAGE_SIZE = (round(WIDTH/28), round(HEIGHT/20))

BLACKPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bpawn.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
BLACKROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-rook.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
BLACKKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-knight.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
BLACKBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bishop.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
BLACKKINGIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-king.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
BLACKQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-queen.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
deadBLACKPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bpawn.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadBLACKROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-rook.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadBLACKKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-knight.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadBLACKBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-bishop.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadBLACKQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'black-queen.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)

WHITEPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bpawn.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
WHITEROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-rook.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
WHITEKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-knight.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
WHITEBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bishop.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
WHITEKINGIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-king.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
WHITEQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-queen.png')).convert_alpha(), DEFAULT_IMAGE_SIZE)
deadWHITEPAWNIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bpawn.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadWHITEROOKIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-rook.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadWHITEKNIGHTIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-knight.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadWHITEBISHOPIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-bishop.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)
deadWHITEQUEENIMAGE = pygame.transform.scale(pygame.image.load(os.path.join('images', 'white-queen.png')).convert_alpha(), DEFAULT_SMALL_IMAGE_SIZE)


def paint(board: chess.Board, currentScrollVal: int, perspectiveWhite: bool, playerWhite: bool):
    screen.fill(DARKSQUARE) # fill screen with color of dark squares
    for m in range(32):
        col = m % 4
        row = m // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*600 - (col*(WIDTH/1400)*200)), round(row * (HEIGHT/1000)*100 + (HEIGHT/1000)*100), round((WIDTH/1400)*100), round((HEIGHT/1000)*100)])
        else:
            pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*700 - (col*(WIDTH/1400)*200)), round(row * (HEIGHT/1000)*100 + (HEIGHT/1000)*100), round((WIDTH/1400)*100), round((HEIGHT/1000)*100)])
        
        
        
        pygame.draw.rect(screen, LIGHTSQUARE, [round(((WIDTH/1400)*800)), round((HEIGHT/1000)*100), round(((WIDTH/1400)*375)), round(((HEIGHT/1000)*800))]) # draw rect outlining move list
        pygame.draw.line(screen, 'black', (0, round((HEIGHT/1000)*100) ), ( round((WIDTH/1400)*1175), round((HEIGHT/1000)*100) ), 4) # draw black outline for top of move list
        drawMoveList(board, currentScrollVal)
        pygame.draw.line(screen, 'black', (0, round((HEIGHT/1000)*900)), (round((WIDTH/1400)*1175), round((HEIGHT/1000)*900) ), 4) # draw black outline for bottom of move list
        pygame.draw.line(screen, 'black', (round((WIDTH/1400)*1175), 0), (round((WIDTH/1400)*1175), HEIGHT), 4) # draw black outline separating menu from move listing
        pygame.draw.line(screen, 'black', (round((WIDTH/1400)*801), 0), (round((WIDTH/1400)*801), HEIGHT), 4) # draw black outline separating menu from game


        # paint darkcolor rectangle underneath buttons
        pygame.draw.rect(screen, (DARKSQUARE), [round((WIDTH/1400)*803), round((HEIGHT/1000)*903), (round((WIDTH/1400)*370)), round((HEIGHT/10))]) 

        # draw new game button
        pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*810), round((HEIGHT/1000)*910), round((WIDTH/1400)*85), round((HEIGHT/1000)*85)]) # draw button outline for new game
        pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*815), round((HEIGHT/1000)*915), round((WIDTH/1400)*75), round((HEIGHT/1000)*75)])
        screen.blit(font.render("NEW", True, 'black'), (round((WIDTH/1400)*829),round((HEIGHT/1000)*935)))
        screen.blit(font.render("GAME", True, 'black'), (round((WIDTH/1400)*822), round((HEIGHT/1000)*955)))

        # draw back button
        pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*900), round((HEIGHT/1000)*910), round((WIDTH/1400)*85), round((HEIGHT/1000)*85)]) 
        pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*905), round((HEIGHT/1000)*915), round((WIDTH/1400)*75), round((HEIGHT/1000)*75)])
        pygame.draw.line(screen, 'black', (round((WIDTH/1400)*920), round((HEIGHT/1000)*950)),(round((WIDTH/1400)*960), round((HEIGHT/1000)*930)), 10)
        pygame.draw.line(screen, 'black', (round((WIDTH/1400)*920), round((HEIGHT/1000)*950)),(round((WIDTH/1400)*960), round((HEIGHT/1000)*970)), 10)

        # draw flip board button
        pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*990), round((HEIGHT/1000)*910), round((WIDTH/1400)*85), round((HEIGHT/1000)*85)]) 
        pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*995), round((HEIGHT/1000)*915), round((WIDTH/1400)*75), round((HEIGHT/1000)*75)])
        screen.blit(font.render("FLIP", True, 'black'), (round((WIDTH/1400)*1010), round((HEIGHT/1000)*935)))
        screen.blit(font.render("BOARD", True, 'black'), (round((WIDTH/1400)*995), round((HEIGHT/1000)*955)))

        # draw hint button
        pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*1080), round((HEIGHT/1000)*910), round((WIDTH/1400)*85), round((HEIGHT/1000)*85)])  
        pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*1085), round((HEIGHT/1000)*915), round((WIDTH/1400)*75), round((HEIGHT/1000)*75)])
        screen.blit(font.render("HINT", True, 'black'), (round((WIDTH/1400)*1099), round((HEIGHT/1000)*940)))
        if playerWhite:
            if perspectiveWhite:
                screen.blit(big_font.render(f"Player: {playername}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*905)))
                screen.blit(big_font.render(f"Player2: {player2name}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*5)))
            else:
                screen.blit(big_font.render(f"Player: {playername}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*5)))
                screen.blit(big_font.render(f"Player2: {player2name}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*905)))
        else:
            if perspectiveWhite:
                screen.blit(big_font.render(f"Player: {playername}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*5)))
                screen.blit(big_font.render(f"Player2: {player2name}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*905)))
            else:
                screen.blit(big_font.render(f"Player: {playername}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*905)))
                screen.blit(big_font.render(f"Player2: {player2name}", True, 'black'), (round((WIDTH/1400)*10), round((HEIGHT/1000)*5)))


        for i in range(0,9): # draw black lines outlining squares
            pygame.draw.line(screen, 'black', (0, round((HEIGHT/1000)*100 + (HEIGHT/1000)*100*i)), (round((WIDTH/1400)*800), round((HEIGHT/1000)*100 + (HEIGHT/1000)*100*i)), 2)
            pygame.draw.line(screen, 'black', (round((WIDTH/1400)*100*i), round((HEIGHT/1000)*100)), (round((WIDTH/1400)*100*i), round((HEIGHT/1000)*900)), 2)

        drawPieces(board, perspectiveWhite)

def drawPieces(board: chess.Board, perspectiveWhite: bool): # draw pieces on board in positons specified by board object

    blackXOffset = round((WIDTH/1400)*10)
    whiteXOffset = round((WIDTH/1400)*10)
    deadPieces = chessApp.boardToDeadPiecesList(board)
    if perspectiveWhite:
        if len(deadPieces) != 0: # draw dead pieces if list is not empty

            # draw dead black pieces next to white players name
            for i in range(deadPieces[9]): # draw black queen if dead
                screen.blit(deadBLACKQUEENIMAGE, (blackXOffset, round((HEIGHT/1000)*950)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[6]): # draw black rooks if dead
                screen.blit(deadBLACKROOKIMAGE, (blackXOffset, round((HEIGHT/1000)*950)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[8]): # draw black bishops if dead
                screen.blit(deadBLACKBISHOPIMAGE, (blackXOffset, round((HEIGHT/1000)*950)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[7]): # draw black knights if dead
                screen.blit(deadBLACKKNIGHTIMAGE, (blackXOffset, round((HEIGHT/1000)*950)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[11]): # draw black pawns if dead
                screen.blit(deadBLACKPAWNIMAGE, (blackXOffset, round((HEIGHT/1000)*950)))
                blackXOffset+=round((WIDTH/1400)*50)

            # draw dead white pieces next to black players name
            for i in range(deadPieces[3]): # draw white queen if dead
                screen.blit(deadWHITEQUEENIMAGE, (whiteXOffset, round((HEIGHT/1000)*50)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[0]): # draw white rooks if dead
                screen.blit(deadWHITEROOKIMAGE, (whiteXOffset, round((HEIGHT/1000)*50)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[2]): # draw white bishops if dead
                screen.blit(deadWHITEBISHOPIMAGE, (whiteXOffset, round((HEIGHT/1000)*50)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[1]): # draw white knights if dead
                screen.blit(deadWHITEKNIGHTIMAGE, (whiteXOffset, round((HEIGHT/1000)*50)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[5]): # draw white pawns if dead
                screen.blit(deadWHITEPAWNIMAGE, (whiteXOffset, round((HEIGHT/1000)*50)))
                whiteXOffset+=round((WIDTH/1400)*50)

        squareList = str(board).split()
        colCount = 0
        rowCount = 0
        for square in squareList:
            # black pieces
            if square == 'r':
                screen.blit(BLACKROOKIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'n':
                screen.blit(BLACKKNIGHTIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'b':
                screen.blit(BLACKBISHOPIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'k':
                screen.blit(BLACKKINGIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'q':
                screen.blit(BLACKQUEENIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'p':
                screen.blit(BLACKPAWNIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            # white pieces
            elif square == 'R':
                screen.blit(WHITEROOKIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'N':
                screen.blit(WHITEKNIGHTIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'B':
                screen.blit(WHITEBISHOPIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'K':
                screen.blit(WHITEKINGIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'Q':
                screen.blit(WHITEQUEENIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'P':
                screen.blit(WHITEPAWNIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            
            

            colCount+=1
            if colCount == 8:
                colCount = 0
                rowCount+=1
    
    else: # persepctive is from black

        if len(deadPieces) != 0: # draw dead pieces if list is not empty

            # draw dead black pieces next to white players name
            for i in range(deadPieces[9]): # draw black queen if dead
                screen.blit(deadBLACKQUEENIMAGE, (blackXOffset, round((HEIGHT/1000)*50)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[6]): # draw black rooks if dead
                screen.blit(deadBLACKROOKIMAGE, (blackXOffset, round((HEIGHT/1000)*50)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[8]): # draw black bishops if dead
                screen.blit(deadBLACKBISHOPIMAGE, (blackXOffset, round((HEIGHT/1000)*50)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[7]): # draw black knights if dead
                screen.blit(deadBLACKKNIGHTIMAGE, (blackXOffset, round((HEIGHT/1000)*50)))
                blackXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[11]): # draw black pawns if dead
                screen.blit(deadBLACKPAWNIMAGE, (blackXOffset, round((HEIGHT/1000)*50)))
                blackXOffset+=round((WIDTH/1400)*50)

            # draw dead white pieces next to black players name
            for i in range(deadPieces[3]): # draw white queen if dead
                screen.blit(deadWHITEQUEENIMAGE, (whiteXOffset, round((HEIGHT/1000)*950)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[0]): # draw white rooks if dead
                screen.blit(deadWHITEROOKIMAGE, (whiteXOffset, round((HEIGHT/1000)*950)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[2]): # draw white bishops if dead
                screen.blit(deadWHITEBISHOPIMAGE, (whiteXOffset, round((HEIGHT/1000)*950)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[1]): # draw white knights if dead
                screen.blit(deadWHITEKNIGHTIMAGE, (whiteXOffset, round((HEIGHT/1000)*950)))
                whiteXOffset+=round((WIDTH/1400)*50)
            for i in range(deadPieces[5]): # draw white pawns if dead
                screen.blit(deadWHITEPAWNIMAGE, (whiteXOffset, round((HEIGHT/1000)*950)))
                whiteXOffset+=round((WIDTH/1400)*50)

        squareList = str(board).split()
        colCount = 7
        rowCount = 7
        for square in squareList:
        # black pieces
            if square == 'r':
                screen.blit(BLACKROOKIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'n':
                screen.blit(BLACKKNIGHTIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'b':
                screen.blit(BLACKBISHOPIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'k':
                screen.blit(BLACKKINGIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'q':
                screen.blit(BLACKQUEENIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'p':
                screen.blit(BLACKPAWNIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            # white pieces
            elif square == 'R':
                screen.blit(WHITEROOKIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'N':
                screen.blit(WHITEKNIGHTIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'B':
                screen.blit(WHITEBISHOPIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'K':
                screen.blit(WHITEKINGIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'Q':
                screen.blit(WHITEQUEENIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
            elif square == 'P':
                screen.blit(WHITEPAWNIMAGE, (colCount*round((WIDTH/1400)*100), rowCount*round((HEIGHT/1000)*100) + (HEIGHT/1000)*100) )
        
        

            colCount-=1
            if colCount == -1:
                colCount=7
                rowCount-=1

def drawValidMoves(mouse: tuple, board: chess.Board, clicked: bool, perspectiveWhite: bool): # draws valid moves on screen when square is clicked
    if perspectiveWhite:
        rowNum = 8
        for row in range(0,8): # loop through all squares to find which one was clicked on
            asciiVal = 97
            for col in range(0,8):
                                
                if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+(WIDTH/1400)*100 and row*round((HEIGHT/1000)*100)+(HEIGHT/1000)*100 <= mouse[1] <= row*round((HEIGHT/1000)*100)+(HEIGHT/1000)*200: # mouseclick is in square
                    legalMoves = chessApp.boardToLegalMoveListUCI(board)
                    occupiedSquaresWithLegalMoves = []
                    for mv in legalMoves:
                        occupiedSquaresWithLegalMoves.append(mv[:2])

                    if (f"{chr(asciiVal)}{rowNum}") in occupiedSquaresWithLegalMoves: 
                        if clicked: # update coordinates of attack squares
                            # display legal moves for square clicked on
                            legalMovesForSquare.clear()
                            targetSquares.clear()
                            for mv in legalMoves:
                                if mv.startswith(f"{chr(asciiVal)}{rowNum}"):
                                    legalMovesForSquare.append(mv)
                                    targetSquares.append(mv[2:])
                            coords.clear()
                            for sq in targetSquares:
                                # convert asciiValue column and row value into list of coordinates to draw circles onto target squares
                                cl = (ord(sq[0])-97) # cols a-h represented as 0-7
                                rw = int(sq[1])-1 # rows 1-8 as 0-7
                                coords.append((cl*round((WIDTH/1400)*100)+(WIDTH/1400)*50, ((HEIGHT/1000)*850)-rw*((HEIGHT/1000)*100)))
                asciiVal+=1
            rowNum-=1
    
    else: # perpective is from blacks side
        rowNum = 1
        for row in range(0,8): # loop through all squares to find which one was clicked on
            asciiVal = 104
            for col in range(0,8):
                                
                if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+(WIDTH/1400)*100 and row*round((HEIGHT/1000)*100)+(HEIGHT/1000)*100 <= mouse[1] <= row*round((HEIGHT/1000)*100)+(HEIGHT/1000)*200: # mouseclick is in square
                    legalMoves = chessApp.boardToLegalMoveListUCI(board)
                    occupiedSquaresWithLegalMoves = []
                    for mv in legalMoves:
                        occupiedSquaresWithLegalMoves.append(mv[:2])

                    if (f"{chr(asciiVal)}{rowNum}") in occupiedSquaresWithLegalMoves: 
                        if clicked: # update coordinates of attack squares
                            # display legal moves for square clicked on
                            legalMovesForSquare.clear()
                            targetSquares.clear()
                            for mv in legalMoves:
                                if mv.startswith(f"{chr(asciiVal)}{rowNum}"):
                                    legalMovesForSquare.append(mv)
                                    targetSquares.append(mv[2:])
                            coords.clear()
                            for sq in targetSquares:
                                # convert asciiValue column and row value into list of coordinates to draw circles onto target squares
                                cl = (ord(sq[0])-97) # cols a-h represented as 0-7
                                rw = int(sq[1])-1 # rows 1-8 as 0-7
                                coords.append(((7-cl)*round((WIDTH/1400)*100)+(WIDTH/1400)*50, ((HEIGHT/1000)*850)-(7-rw)*((HEIGHT/1000)*100)))
                asciiVal-=1
            rowNum+=1
    if len(coords) != 0:  
        for coord in coords:
            pygame.draw.circle(screen, (255,1,1), (coord[0], coord[1]), 10)

def drawHint(board: chess.Board, perspectiveWhite: bool): # best move contains zero or 1 string at all times
    if perspectiveWhite:
        bm = currentBestMove[0]
        originSq = bm[:2]
        sq = bm[2:]
        cl = (ord(sq[0])-97) # cols a-h represented as 0-7
        rw = int(sq[1])-1 # rows 1-8 as 0-7
        ocl = (ord(originSq[0])-97) # cols a-h represented as 0-7
        orw = int(originSq[1])-1 # rows 1-8 as 0-7
        pygame.draw.circle(screen, (255,1,1), (cl*((WIDTH/1400)*100)+((WIDTH/1400)*50), ((HEIGHT/1000)*850)-rw*((HEIGHT/1000)*100)), 10)
        pygame.draw.circle(screen, (0,255,0), (ocl*round((WIDTH/1400)*100)+round((WIDTH/1400)*50), round((HEIGHT/1000)*850)-orw*round((HEIGHT/1000)*100)), 10)
    else:
        bm = currentBestMove[0]
        originSq = bm[:2]
        sq = bm[2:]
        cl = (ord(sq[0])-97) # cols a-h represented as 0-7
        rw = int(sq[1])-1 # rows 1-8 as 0-7
        ocl = (ord(originSq[0])-97) # cols a-h represented as 0-7
        orw = int(originSq[1])-1 # rows 1-8 as 0-7
        pygame.draw.circle(screen, (255,1,1), ((7-cl)*((WIDTH/1400)*100)+((WIDTH/1400)*50), ((HEIGHT/1000)*850)-(7-rw)*((HEIGHT/1000)*100)), 10)
        pygame.draw.circle(screen, (0,255,0), ((7-ocl)*round((WIDTH/1400)*100)+round((WIDTH/1400)*50), round((HEIGHT/1000)*850)-(7-orw)*round((HEIGHT/1000)*100)), 10)

def handleUIclicks(board, mouse: tuple, currentFenListIndex: list) -> str:
    if round((WIDTH/1400)*815) <= mouse[0] <= round((WIDTH/1400)*890) and round((HEIGHT/1000)*915) <= mouse[1] <= round((HEIGHT/1000)*990): # clicked on new game button
        board.reset()
        board.clear_stack()
        moveList.clear()
        currentBestMove.clear()
        currentBestMove.append(AI.bestMove(board))
        return "new"
    elif round((WIDTH/1400)*905) <= mouse[0] <= round((WIDTH/1400)*980) and round((HEIGHT/1000)*915) <= mouse[1] <= round((HEIGHT/1000)*990): # clicked on back button
        # implement ability to go backwards in move list
        if len(fenList) > 0 and 0 <= currentFenListIndex[0]-2 < len(fenList):
            currentFenListIndex[0]-=2 # in place change on currentFenListIndex defined in main
            # remove moves from move list
            if len(moveList) > 0:
                if (not (board.is_checkmate() or board.is_stalemate())) and len(moveList) > 1:
                    moveList.pop(len(moveList)-1)
                    if len(moveList) > 1:
                        moveList.pop(len(moveList)-1)
                    board.pop() 
                    board.pop()
                    currentBestMove.clear()
                    currentBestMove.append(AI.bestMove(board))
            return "back"
    elif round((WIDTH/1400)*995) <= mouse[0] <= round((WIDTH/1400)*1070) and round((HEIGHT/1000)*915) <= mouse[1] <= round((HEIGHT/1000)*990): # clicked on flip board button
        legalMovesForSquare.clear()
        targetSquares.clear()
        coords.clear()
        return "flip"
    elif round((WIDTH/1400)*1085) <= mouse[0] <= round((WIDTH/1400)*1160) and round((HEIGHT/1000)*915) <= mouse[1] <= round((HEIGHT/1000)*990): # clicked on hint button
        # highlight attack square returned by
        coords.clear()
        targetSquares.clear()
        legalMovesForSquare.clear()
        return "hint"
    return ""

def handlePromotionSelection(board: chess.Board, mouse: tuple, move: str, currentFenListIndex: list, currentScrollVal: int, perspectiveWhite: bool, playerWhite: bool) -> str: # returns empty string when promotion selection has been made to update isPromotion variable in main()
    
    
    if round((WIDTH/1400)*200) <= mouse[0] <= round((WIDTH/1400)*600) and  round((HEIGHT/1000)*400) <= mouse[1] <= round((HEIGHT/1000)*500): # if click in selection box

        if round((WIDTH/1400)*200) <= mouse[0] <= round((WIDTH/1400)*300) and  round((HEIGHT/1000)*400) <= mouse[1] <= round((HEIGHT/1000)*500): # click in queen box

            mv = move[:4]+"q"
            fenList.append(board.fen()) # append to fenList before player move made
            moveList.append(board.san(board.parse_uci(mv)))
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
            board.push_uci(mv) # make player move
            fenList.append(board.fen()) # append to fenList after player move made
        
        elif round((WIDTH/1400)*300) <= mouse[0] <= round((WIDTH/1400)*400) and  round((HEIGHT/1000)*400) <= mouse[1] <= round((HEIGHT/1000)*500): # click in rook box
            mv = move[:4]+"r"
            fenList.append(board.fen()) # append to fenList before player move made
            moveList.append(board.san(board.parse_uci(mv)))
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
            board.push_uci(mv) # make player move
            fenList.append(board.fen()) # append to fenList after player move made
            
        elif round((WIDTH/1400)*400) <= mouse[0] <= round((WIDTH/1400)*500) and  round((HEIGHT/1000)*400) <= mouse[1] <= round((HEIGHT/1000)*500): # click in bishop box
            mv = move[:4]+"b"
            fenList.append(board.fen()) # append to fenList before player move made
            moveList.append(board.san(board.parse_uci(mv)))
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
            board.push_uci(mv) # make player move
            fenList.append(board.fen()) # append to fenList after player move made
            
        elif round((WIDTH/1400)*500) <= mouse[0] <= round((WIDTH/1400)*600) and  round((HEIGHT/1000)*400) <= mouse[1] <= round((HEIGHT/1000)*500): # click in knight box
            mv = move[:4]+"n"
            fenList.append(board.fen()) # append to fenList before player move made
            moveList.append(board.san(board.parse_uci(mv)))
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
            board.push_uci(mv) # make player move
            fenList.append(board.fen()) # append to fenList after player move made
        
        # update display
        paint(board, currentScrollVal, perspectiveWhite, playerWhite)
        pygame.display.flip()

        if not (board.is_checkmate() or board.is_stalemate()): # if not checkmate or stalemate make AI response move
            aiMove = AI.getMove(board, 1)
            moveList.append(board.san(board.parse_uci(aiMove)))

            board.push_uci(aiMove) # make move for AI

            fenList.append(board.fen())# append to fenList before AI move made
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
                            
        legalMovesForSquare.clear()
        targetSquares.clear()
        coords.clear()

        currentBestMove.clear()
        currentBestMove.append(AI.bestMove(board))
        return ""
    return move

def drawPromotionSelection(playerWhite: bool):
    # draw box
    pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*195), round((HEIGHT/1000)*395), round((WIDTH/1400)*410), round((HEIGHT/1000)*110)])
    pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*200), round((HEIGHT/1000)*400), round((WIDTH/1400)*400), round((HEIGHT/1000)*100)])
    pygame.draw.line(screen, 'black', (round((WIDTH/1400)*300), round((HEIGHT/1000)*395)), (round((WIDTH/1400)*300), round((HEIGHT/1000)*500)), 3)
    pygame.draw.line(screen, 'black', (round((WIDTH/1400)*400), round((HEIGHT/1000)*395)), (round((WIDTH/1400)*400), round((HEIGHT/1000)*500)), 3)
    pygame.draw.line(screen, 'black', (round((WIDTH/1400)*500), round((HEIGHT/1000)*395)), (round((WIDTH/1400)*500), round((HEIGHT/1000)*500)), 3)
    if playerWhite:
        # draw Queen 
        screen.blit(WHITEQUEENIMAGE, (round((WIDTH/1400)*195), round((HEIGHT/1000)*395)) )
        # draw Rook 
        screen.blit(WHITEROOKIMAGE, (round((WIDTH/1400)*295), round((HEIGHT/1000)*395)) )
        # draw Bishop 
        screen.blit(WHITEBISHOPIMAGE, (round((WIDTH/1400)*395), round((HEIGHT/1000)*395)) )
        # draw Knight
        screen.blit(WHITEKNIGHTIMAGE, (round((WIDTH/1400)*495), round((HEIGHT/1000)*395)) )
    else:
        # draw Queen 
        screen.blit(BLACKQUEENIMAGE, (round((WIDTH/1400)*195), round((HEIGHT/1000)*395)) )
        # draw Rook 
        screen.blit(BLACKROOKIMAGE, (round((WIDTH/1400)*295), round((HEIGHT/1000)*395)) )
        # draw Bishop 
        screen.blit(BLACKBISHOPIMAGE, (round((WIDTH/1400)*395), round((HEIGHT/1000)*395)) )
        # draw Knight
        screen.blit(BLACKKNIGHTIMAGE, (round((WIDTH/1400)*495), round((HEIGHT/1000)*395)) )

def makeAImove(board: chess.Board, currentFenListIndex: list):
    if (not (board.is_checkmate() or board.is_stalemate())) and board.turn == chess.WHITE:
            aiMove = AI.getMove(board, 1)  # AI difficulty at 1/20
            moveList.append(board.san(board.parse_uci(aiMove)))

            board.push_uci(aiMove) # make move for AI

            fenList.append(board.fen())# append to fenList before AI move made
            currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
            currentBestMove.clear()
            currentBestMove.append(AI.bestMove(board))

def handleAttack(mouse: tuple, board: chess.Board, currentScrollVal: int, currentFenListIndex: list, perspectiveWhite: bool, playerWhite: bool) -> str: # handles mouse events where attack square is clicked and returns uci move if clicked move was a promotion else retruns empty string
    if playerWhite:
        if perspectiveWhite:
            rowNum = 8
            for row in range(0,8): # loop through all squares to find which one was clicked on
                asciiVal = 97
                for col in range(0,8):
                    if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+round((WIDTH/1400)*100) and row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*100) <= mouse[1] <= row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*200): # mouseclick is in square
                        for mv in legalMovesForSquare:
                            if len(mv) == 4: # handle all uci moves with 4 characters, meaning every move but pawn promotion is handled
                                if mv[2:] == f"{chr(asciiVal)}{rowNum}":
                                    
                                    fenList.append(board.fen()) # append to fenList before player move made
                                    moveList.append(board.san(board.parse_uci(mv)))
                                    currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
                                    board.push_uci(mv) # make player move

                                    fenList.append(board.fen()) # append to fenList after player move made
                                    
                                    # update display
                                    paint(board, currentScrollVal, perspectiveWhite, playerWhite)
                                    pygame.display.flip()

                                    if not (board.is_checkmate() or board.is_stalemate()):
                                        aiMove = AI.getMove(board, 1)  # AI difficulty at 1/20
                                        moveList.append(board.san(board.parse_uci(aiMove)))

                                        board.push_uci(aiMove) # make move for AI

                                        fenList.append(board.fen())# append to fenList before AI move made
                                        currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
                                    
                                    legalMovesForSquare.clear()
                                    targetSquares.clear()
                                    coords.clear()

                                    currentBestMove.clear()
                                    currentBestMove.append(AI.bestMove(board))
                                    
                            if len(mv) == 5: # uci move is a pawn promotion
                                if mv[2]+mv[3] == f"{chr(asciiVal)}{rowNum}":
                                    return mv
                    asciiVal+=1
                rowNum-=1
            return ""
        
        else: # perspective is from blacks side
            rowNum = 1
            for row in range(0,8): # loop through all squares to find which one was clicked on
                asciiVal = 104
                for col in range(0,8):
                    if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+round((WIDTH/1400)*100) and row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*100) <= mouse[1] <= row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*200): # mouseclick is in square
                        for mv in legalMovesForSquare:
                            if len(mv) == 4: # handle all uci moves with 4 characters, meaning every move but pawn promotion is handled
                                if mv[2:] == f"{chr(asciiVal)}{rowNum}":
                                    
                                    fenList.append(board.fen()) # append to fenList before player move made
                                    moveList.append(board.san(board.parse_uci(mv)))
                                    currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
                                    board.push_uci(mv) # make player move

                                    fenList.append(board.fen()) # append to fenList after player move made
                                    
                                    # update display
                                    paint(board, currentScrollVal, perspectiveWhite, playerWhite)
                                    pygame.display.flip()

                                    if not (board.is_checkmate() or board.is_stalemate()):
                                        aiMove = AI.getMove(board, 1)  # AI difficulty at 1/20
                                        moveList.append(board.san(board.parse_uci(aiMove)))

                                        board.push_uci(aiMove) # make move for AI

                                        fenList.append(board.fen())# append to fenList before AI move made
                                        currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main
                                    
                                    legalMovesForSquare.clear()
                                    targetSquares.clear()
                                    coords.clear()

                                    currentBestMove.clear()
                                    currentBestMove.append(AI.bestMove(board))
                                    
                            if len(mv) == 5: # uci move is a pawn promotion
                                if mv[2]+mv[3] == f"{chr(asciiVal)}{rowNum}":
                                    return mv
                    asciiVal-=1
                rowNum+=1
            return ""
    
    else: # player is black
        # make AI move
        makeAImove(board, currentFenListIndex)

        if perspectiveWhite:
            rowNum = 8
            for row in range(0,8): # loop through all squares to find which one was clicked on
                asciiVal = 97
                for col in range(0,8):
                    if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+round((WIDTH/1400)*100) and row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*100) <= mouse[1] <= row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*200): # mouseclick is in square
                        for mv in legalMovesForSquare:
                            if len(mv) == 4: # handle all uci moves with 4 characters, meaning every move but pawn promotion is handled
                                if mv[2:] == f"{chr(asciiVal)}{rowNum}":
                                    
                                    moveList.append(board.san(board.parse_uci(mv)))
                                    
                                    board.push_uci(mv) # make player move

                                    fenList.append(board.fen()) # append to fenList after player move made
                                    currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main

                                    # update display
                                    paint(board, currentScrollVal, perspectiveWhite, playerWhite)
                                    pygame.display.flip()


                                    
                                    legalMovesForSquare.clear()
                                    targetSquares.clear()
                                    coords.clear()

                                    
                                    
                            if len(mv) == 5: # uci move is a pawn promotion
                                if mv[2]+mv[3] == f"{chr(asciiVal)}{rowNum}":
                                    return mv
                    asciiVal+=1
                rowNum-=1
            return ""
        
        else: # perspective is from blacks side
            rowNum = 1
            for row in range(0,8): # loop through all squares to find which one was clicked on
                asciiVal = 104
                for col in range(0,8):
                    if col*round((WIDTH/1400)*100) <= mouse[0] <= col*round((WIDTH/1400)*100)+round((WIDTH/1400)*100) and row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*100) <= mouse[1] <= row*round((HEIGHT/1000)*100)+round((HEIGHT/1000)*200): # mouseclick is in square
                        for mv in legalMovesForSquare:
                            if len(mv) == 4: # handle all uci moves with 4 characters, meaning every move but pawn promotion is handled
                                if mv[2:] == f"{chr(asciiVal)}{rowNum}":
                                    
                                    moveList.append(board.san(board.parse_uci(mv)))
                                    
                                    board.push_uci(mv) # make player move

                                    fenList.append(board.fen()) # append to fenList after player move made
                                    currentFenListIndex[0]+=1 # in place change on currentFenListIndex defined in main

                                    # update display
                                    paint(board, currentScrollVal, perspectiveWhite, playerWhite)
                                    pygame.display.flip()


                                    
                                    legalMovesForSquare.clear()
                                    targetSquares.clear()
                                    coords.clear()
                                    
                            if len(mv) == 5: # uci move is a pawn promotion
                                if mv[2]+mv[3] == f"{chr(asciiVal)}{rowNum}":
                                    return mv
                    asciiVal-=1
                rowNum+=1
            return ""


def drawMoveList(board: chess.Board, currentScrollVal):
    moveSurface = pygame.Surface((round((WIDTH/1400)*335), round((HEIGHT/1000)*4000)))
    moveSurface.fill(LIGHTSQUARE)
    yOffset = 0
    turnNum = len(moveList) // 2 + 1
    counter = 1
    for i in range(0, len(moveList), 2):
        moveSurface.blit(font.render(f"{counter}:    {moveList[i]}", True, 'black'), (0, yOffset))
        if i+1 < len(moveList):
            moveSurface.blit(font.render(f"{moveList[i+1]}", True, 'black'), (round((WIDTH/1400)*150), yOffset))
            yOffset+=round((HEIGHT/1000)*30)
        counter+=1
    if currentScrollVal <= 0 and turnNum > 25: # unlock scrolling after 25 moves listed
        if currentScrollVal*45 < -(turnNum)*20:
            moveSurface.scroll(0,-(turnNum)*20)
            currentScrollVal-=1
        else:
            moveSurface.scroll(0, currentScrollVal*45)
    screen.blit(moveSurface,(round((WIDTH/1400)*820), round((HEIGHT/1000)*120)))


def gameOver(board: chess.Board, checkMate: bool): # display checkmate popup
    pygame.draw.rect(screen, (0,0,0), [round((WIDTH/1400)*250), round((HEIGHT/1000)*425), round((WIDTH/1400)*300), round((HEIGHT/1000)*90)])
    pygame.draw.rect(screen, LIGHTSQUARE, [round((WIDTH/1400)*255), round((HEIGHT/1000)*430), round((WIDTH/1400)*290), round((HEIGHT/1000)*80)])
    if checkMate:
        screen.blit(big_font.render("Checkmate!", True, 'black'), (round((WIDTH/1400)*300), round((HEIGHT/1000)*450)))
    else:
        screen.blit(big_font.render("Stalemate!", True, 'black'), (round((WIDTH/1400)*300), round((HEIGHT/1000)*450)))
    pygame.display.flip()


def main(board: chess.Board):
    playerWhite = True # bool to represent the color of player for current game
    perspectiveWhite = True # whites view of the board is true blacks is false
    currentFenListIndex = [0]
    currentBestMove.append(AI.bestMove(board))
    isPromotion = "" # isPromotion is a string that when empty indicates no pawn promotion to be selected and if full contains a length 5 string containing the uci for a promotion move
    UIresponse = "" # tracks which UI buttons have been clicked
    currentScrollVal = 0
    while board.is_game_over:
        timer.tick(fps)
        mouse = pygame.mouse.get_pos() # get mouse coordinates
        paint(board, currentScrollVal, perspectiveWhite, playerWhite)
        
        
        if UIresponse == "hint" and not (board.is_checkmate() or board.is_stalemate()):
            drawHint(board, perspectiveWhite)
        elif UIresponse == "flip":
            perspectiveWhite = not perspectiveWhite
            UIresponse = ""
        elif UIresponse == "new":
            rand = random.randint(0,1)
            if rand == 1:
                playerWhite = True
                perspectiveWhite = True
            else:
                playerWhite = False
                perspectiveWhite = False
            UIresponse = ""

        if not playerWhite:
            makeAImove(board, currentFenListIndex)

        if len(isPromotion) == 5:
            drawPromotionSelection(playerWhite)
            
        if board.is_checkmate():
            gameOver(board,True)
        if board.is_stalemate():
            gameOver(board, False)
        if len(targetSquares) != 0:
            drawValidMoves(mouse,board,False, perspectiveWhite) # draws currently selected attack squares

        for event in pygame.event.get(): # capture all pygame events in a continuous loop at 60fps
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # if left click
                drawValidMoves(mouse,board,True, perspectiveWhite)
                if len(isPromotion) != 5:
                    isPromotion = handleAttack(mouse, board, currentScrollVal, currentFenListIndex, perspectiveWhite, playerWhite) 
                    UIresponse = handleUIclicks(board, mouse, currentFenListIndex)
            
                if len(isPromotion) == 5:
                    isPromotion = handlePromotionSelection(board, mouse, isPromotion, currentFenListIndex, currentScrollVal, perspectiveWhite, playerWhite)

                
            if event.type == pygame.MOUSEWHEEL: # if mousewheel is up or down scroll movelist
                if event.y == -1:
                    currentScrollVal-=1
                elif event.y == 1:
                    currentScrollVal+=1
                
        pygame.display.flip()
    pygame.quit()

board = chess.Board()
main(board)