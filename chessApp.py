import chess
import chess.svg
import AI


# Helper Functions
def boardToDeadPiecesList(board: chess.Board) -> list: # takes in a board object and returns list of number of dead pieces if there are any else it returns an empty list
    r, n, b, q, k, p = 0, 0, 0, 0, 0, 0
    wr, wn, wb, wq, wk, wp = 0, 0, 0, 0, 0, 0
    aliveWhitePiecesList = []
    aliveBlackPiecesList = []
    
    totalAlivePieces = 0
    fen = board.fen()
    rowCount = 8
    colCount = 8
    for chr in fen:
        if 97 <= ord(chr) <= 122: #lower case letter indicates black piece in FEN string
            aliveBlackPiecesList.append(chr)
            totalAlivePieces +=1
        elif 65 <= ord(chr) <= 90:
            aliveWhitePiecesList.append(chr)
            totalAlivePieces +=1
        if ord(chr) == 47 or ord(chr) == 32: # if equals backslash or space decrement rowCount
            rowCount-=1
        if rowCount == 0:
            break

    for piece in aliveBlackPiecesList: # tally variables corresponding to piece counts
        if piece == 'r':
            r+=1
        elif piece == 'n':
            n+=1
        elif piece == 'b':
            b+=1
        elif piece == 'q':
            q+=1
        elif piece == 'k':
            k+=1
        elif piece == 'p':
            p+=1
    for piece in aliveWhitePiecesList: # tally variables corresponding to piece counts
        if piece == 'R':
            wr+=1
        elif piece == 'N':
            wn+=1
        elif piece == 'B':
            wb+=1
        elif piece == 'Q':
            wq+=1
        elif piece == 'K':
            wk+=1
        elif piece == 'P':
            wp+=1
    #print(wr, wn, wb, wq, wk, wp, r, n, b, q, k, p)
    deadPiecesList = [2-wr, 2-wn, 2-wb, 1-wq, 1-wk, 8-wp, 2-r, 2-n, 2-b, 1-q, 1-k, 8-p] # indexes 0-5 for Whites, 6-11 for Blacks
    
    if totalAlivePieces < 32:
        return deadPiecesList
    else:
        return []

def boardWithLabels(board: chess.Board, flipped: bool) -> str: # returns a string representing chess board with rows and columns labeled and can optionally be flipped to show the black player's view of the board

    labeledBoard = "\n     H G F E D C B A\n"
    boardList = str(board).split()

    if (not flipped):
        labeledBoard = "\n     A B C D E F G H\n"
        colCount = 7
        rowCount = 8
        for char in boardList:
            if (colCount == 7):
                labeledBoard += (f"\n{rowCount}    {char}")
                rowCount-=1
                colCount = 0
            else:
                labeledBoard += (f" {char}")
                colCount += 1

    # reverse view of white player
    else: 
        colCount = 7
        rowCount = 1
        for index in range(63,-1,-1):
            if (colCount == 7):
                labeledBoard += (f"\n{rowCount}    {boardList[index]}")
                rowCount+=1
                colCount = 0
            else:
                labeledBoard += (f" {boardList[index]}")
                colCount += 1
    
    return labeledBoard

def boardToLegalMoveListUCI(board: chess.Board) -> list: # Turns LegalMoveGenerator returned by board.legal_moves into a list of legal moves using uci notation Ex: Legal Moves: ['g1h3', 'g1f3', 'b1c3', 'b1a3', 'h2h3', 'g2g3', 'f2f3', 'e2e3', 'd2d3', 'c2c3', 'b2b3', 'a2a3', 'h2h4', 'g2g4', 'f2f4', 'e2e4', 'd2d4', 'c2c4', 'b2b4', 'a2a4']
    mvlist = list(board.legal_moves)
    uciList = []
    for mv in mvlist:
        uciList.append(mv.uci())
    return uciList




