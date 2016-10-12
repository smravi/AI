import sys
import timeit

def isBoardComplete(board, matrixDimension):
    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if board[i][j] == '.':
                return False
    return True

def getEvalScore(board, gameCell, player, matrixDimension):
    # person can be a player or opponent
    # calculate the player score
    playerScore = 0
    opponentScore = 0
    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if board[i][j] != '.':
                if board[i][j] == player:
                    playerScore += gameCell[i][j]
                else:
                    opponentScore += gameCell[i][j]
    evalValue = playerScore - opponentScore
    return evalValue

def main():
    #isBoardComplete([['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', 'X'], ['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', '.'], ['.', '.', '.', '.', '.']], 5)
    getEvalScore([['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', 'X'], ['.', '.', 'X', 'X', '.'], ['.', '.', 'X', 'O', '.'], ['.', '.', '.', '.', '.']], [[20, 16, 1, 32, 30], [20, 12, 2, 11, 8], [28, 48, 9, 1, 1], [20, 12, 10, 6, 2], [25, 30, 23, 21, 10]], 'X', 5)
if __name__ == '__main__':
    # main()
    exec_time = '{:.2f}s'.format(timeit.timeit("main()",
                                               setup="from __main__ import main", number=804050))
    print(exec_time)
