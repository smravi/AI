import queue
from collections import namedtuple
import timeit

NextMove = namedtuple('NextMove', 'iIndex jIndex moveType')

def isPositionEmpty(board, i, j):
    if board[i][j] == '.':
        return True
    return False

def isInRange(iValue, jValue, matrixDimension):
    return 0 <= iValue <= matrixDimension - 1 and 0 <= jValue <= matrixDimension - 1

def isValidStake(playerBoard, i, j, matrixDimension, player):
    if isInRange(i, j - 1, matrixDimension) and playerBoard[i][j - 1] == player:
        return False
    if isInRange(i, j + 1, matrixDimension) and playerBoard[i][j + 1] == player:
        return False
    if isInRange(i + 1, j, matrixDimension) and playerBoard[i + 1][j] == player:
        return False
    if isInRange(i - 1, j, matrixDimension) and playerBoard[i - 1][j] == player:
        return False
    return True

def createMoveQueue(playerBoard, matrixDimension, currentPlayer):
    movequeue = queue.Queue()
    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if isPositionEmpty(playerBoard, i, j):
                movequeue.put(NextMove(i, j, 'Stake'))
    for moveElement in list(movequeue.queue):
        if not isValidStake(playerBoard, moveElement.iIndex, moveElement.jIndex, matrixDimension, currentPlayer):
            movequeue.put(NextMove(moveElement.iIndex, moveElement.jIndex, 'Raid'))
    return movequeue

def main():
    createMoveQueue(
        [['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', 'X'], ['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', '.'],
         ['.', '.', '.', '.', '.']], 5, 'X')

exec_time = '{:.2f}s'.format(timeit.timeit("main()",
                                           setup="from __main__ import main", number=800000))
