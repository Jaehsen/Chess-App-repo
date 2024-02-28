import chess
import chessApp
import random
from stockfish import Stockfish

# AI functions
def randomMove(board: chess.Board):
    legalMoves = chessApp.boardToLegalMoveListUCI(board) # turns LegalMoveGenerator into a list of legal moves
    rand = random.randint(0,len(legalMoves)-1)
    return legalMoves[rand]

def bestMove(board: chess.Board) -> str:
    stockfish = Stockfish("stockfish\stockfish-windows-x86-64-avx2.exe")
    stockfish.set_depth(20)
    stockfish.set_skill_level(20)
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()

def getMove(board: chess.Board, difficulty: int) -> str: # difficulty levels 1-20
    stockfish = Stockfish("stockfish\stockfish-windows-x86-64-avx2.exe")
    stockfish.set_depth(difficulty)
    stockfish.set_skill_level(difficulty)
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()
    