"""
This module contains the AI Functions that the program uses. 
"""


import chess
import chessApp
import random
from stockfish import Stockfish


def getRandomMove(board: chess.Board):
    """
    Returns a random possible move from the avalible moves.

    Args:
        board (chess.Board): The board of the current game state.

    Returns:
        str: a random legal move.
    """
    legalMoves = chessApp.boardToLegalMoveListUCI(board)
    return random.choice(legalMoves)


def bestMove(board: chess.Board) -> str:
    """
    Returns the best possible move based on a depth of 20, a skill level of 20, and the current board state
    Args:
        board (chess.Board): The board of the current game state.

    Returns:
         str: The best legal move. 
    """
    stockfish = Stockfish("stockfish\stockfish-windows-x86-64-avx2.exe")
    stockfish.set_depth(20)
    stockfish.set_skill_level(20)
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()


def getMove(board: chess.Board, difficulty: int) -> str:
    """
    Returns the best possible move based on a given depth and skill level difficulty from 1-20, and the current board state

    Args:
        board (chess.Board): The board of the current game state.
        difficulty (int): The value that will be passed as the depth and skill level.

    Returns:
         str: The best legal move based on the given difficulty. 
    """
    stockfish = Stockfish("stockfish\stockfish-windows-x86-64-avx2.exe")
    stockfish.set_depth(difficulty)
    stockfish.set_skill_level(difficulty)
    stockfish.set_fen_position(board.fen())
    return stockfish.get_best_move()
    