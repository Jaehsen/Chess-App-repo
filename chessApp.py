"""
This module contains helper methods for the 
"""


import chess
import chess.svg
import AI

# Helper Functions
def getDeadPieces(board: chess.Board) -> list[chess.Piece]:
    """
    Returns a list of which peices are dead in the following order: pawn bishop knight rook queen.
    
    Args:
        board (chess.Board): the board of the current game state.

    Returns:
        List (chess.Piece): The list of the current dead pieces.
    """
    deadPieces:list[chess.Piece]=list(chess.BaseBoard().piece_map().values())
    deadPieces.sort(key=order)
    for value in list(board.piece_map().values()):
        try:
            deadPieces.remove(value)
        except Exception as e:
            pass #user promoted pawns to create more of a piece type than there are on the base board
    return deadPieces


def order(piece: chess.Piece) -> int:
    """
    Takes a chess.Piece and converts it from an int (1-6) to an int (0-5).

    Args:
        piece (chess.Piece): a chess piece that will converted to an int int the range (0-5).

    Returns:
        int: The given value of a chess piece.
    """
    if piece.piece_type==chess.PAWN:
        return 0
    if piece.piece_type==chess.BISHOP:
        return 1
    if piece.piece_type==chess.KNIGHT:
        return 2
    if piece.piece_type==chess.ROOK:
        return 3
    if piece.piece_type==chess.QUEEN:
        return 4
    return 5

def boardWithLabels(board: chess.Board, flipped: bool) -> str: 
    """
    Returns a string representing the chess board with rows and columns labeled, 
    which can be flipped to show the black player's view of the board.

    Args: 
        board (chess.Board): The board of the currant game state.
        flipped (bool): Boolean to determine if the board should be flipped.

    Returns:
        str: the board in a string representing the chess board.
    """

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


def boardToLegalMoveListUCI(board: chess.Board) -> list: 
    """
    Turns LegalMoveGenerator returned by board.legal_moves into a list of legal moves using uci notation 
    Ex: Legal Moves: ['g1h3', 'g1f3', 'b1c3', 'b1a3', 'h2h3', 'g2g3', 'f2f3', 'e2e3', 'd2d3', 'c2c3', 'b2b3',
    'a2a3', 'h2h4', 'g2g4', 'f2f4', 'e2e4', 'd2d4', 'c2c4', 'b2b4', 'a2a4'].
    
    Args:
        board (chess.Board): The board of the currant game state.

    Returns:
        List (Move): The List of all available moves in uci notation.
    
    """
    mvlist = list(board.legal_moves)
    uciList = []
    for mv in mvlist:
        uciList.append(mv.uci())
    return uciList
