import sys
import math
import copy
import timeit


def writeOutput(fileName, state, boardState):
    with open(fileName, 'w') as f:
        f.write('{}\n'.format(state))
        for i, row in enumerate(boardState):
            for j, col in enumerate(row):
                f.write(boardState[i][j])
            f.write('\n')
        f.truncate(f.tell() - 1)


def isBoardComplete(board, matrixDimension):
    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if board[i][j] == '.':
                return False
    return True


def isInRange(iValue, jValue, matrixDimension):
    return 0 <= iValue <= matrixDimension - 1 and 0 <= jValue <= matrixDimension - 1


def getOpponent(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'


def isPositionEmpty(board, i, j):
    if board[i][j] == '.':
        return True
    return False


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
    # return Gamescore(evalValue, player, playerScore, getOpponent(player), opponentScore)


def setPosition(board, i, j, player):
    if isPositionEmpty(board, i, j):
        board[i][j] = player


def revertPosition(board, i, j, player):
    if board[i][j] == player:
        board[i][j] = '.'


def getStakeScore(gameCell, i, j):
    return gameCell[i][j]


def isValidStake(boardState, i, j, matrixDimension, player):
    if isInRange(i, j - 1, matrixDimension) and boardState[i][j - 1] == player:
        return False
    if isInRange(i, j + 1, matrixDimension) and boardState[i][j + 1] == player:
        return False
    if isInRange(i + 1, j, matrixDimension) and boardState[i + 1][j] == player:
        return False
    if isInRange(i - 1, j, matrixDimension) and boardState[i - 1][j] == player:
        return False
    return True


# def isRaidValid(boardState, i, j, matrixDimension, currentPlayer):


def markRaidPositions(boardState, i, j, matrixDimension, currentPlayer):
    opponent = getOpponent(currentPlayer)
    if isInRange(i, j - 1, matrixDimension) and boardState[i][j - 1] == opponent:
        boardState[i][j - 1] = currentPlayer
    if isInRange(i, j + 1, matrixDimension) and boardState[i][j + 1] == opponent:
        boardState[i][j + 1] = currentPlayer
    if isInRange(i + 1, j, matrixDimension) and boardState[i + 1][j] == opponent:
        boardState[i + 1][j] = currentPlayer
    if isInRange(i - 1, j, matrixDimension) and boardState[i - 1][j] == opponent:
        boardState[i - 1][j] = currentPlayer


def minimax(boardState, gameCell, matrixDimension, moveMaker, currentPlayer, depthLimit, currentDepth):
    iTile = -1
    jTile = -1
    if currentDepth % 2 == 0:
        evalValue = -math.inf
    else:
        evalValue = math.inf

    # break recursion
    if currentDepth == depthLimit or isBoardComplete(boardState, matrixDimension):
        evalValue = getEvalScore(boardState, gameCell, moveMaker, matrixDimension)
        return evalValue, iTile, jTile
    # maximizer is in position 0,2,4

    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if isPositionEmpty(boardState, i, j):
                # localBoard = copy.deepcopy(boardState)
                localBoard = [eachRow[:] for eachRow in boardState]
                if isValidStake(localBoard, i, j, matrixDimension, currentPlayer):
                    # Stake move
                    localBoard[i][j] = currentPlayer
                else:
                    # Possibility of raid move so mark the neighboring states and pass down
                    localBoard[i][j] = currentPlayer
                    markRaidPositions(localBoard, i, j, matrixDimension, currentPlayer)

                utility, unused1, unused2 = minimax(localBoard, gameCell, matrixDimension, moveMaker,
                                                    getOpponent(currentPlayer),
                                                    depthLimit, currentDepth + 1)
                # We are in maximiser
                if currentDepth % 2 == 0:
                    #                    if utility > evalValue and utility > alpha:
                    if utility > evalValue:
                        evalValue = utility
                        # if you are the maximizer node, then you should change the position of the next tile to consider
                        if currentDepth == 0:
                            iTile = i
                            jTile = j
                # We are in minimizer
                else:
                    #                    if utility < evalValue and utility < beta:
                    if utility < evalValue:
                        evalValue = utility
    return evalValue, iTile, jTile


def alphaBeta(boardState, gameCell, matrixDimension, moveMaker, currentPlayer, depthLimit, currentDepth, alpha, beta):
    iTile = -1
    jTile = -1

    if currentDepth % 2 == 0:
        evalValue = -math.inf
    else:
        evalValue = math.inf

    # break recursion
    if currentDepth == depthLimit or isBoardComplete(boardState, matrixDimension):
        evalValue = getEvalScore(boardState, gameCell, moveMaker, matrixDimension)
        return evalValue, iTile, jTile
    # maximizer is in position 0,2,4
    prune = False
    for i in range(matrixDimension):
        if prune:
            break
        for j in range(matrixDimension):
            if isPositionEmpty(boardState, i, j):

                # localBoard = copy.deepcopy(boardState)
                localBoard = [eachRow[:] for eachRow in boardState]

                if isValidStake(localBoard, i, j, matrixDimension, currentPlayer):
                    # Stake move
                    localBoard[i][j] = currentPlayer
                else:
                    # Possibility of raid move so mark the neighboring states and pass down
                    localBoard[i][j] = currentPlayer
                    markRaidPositions(localBoard, i, j, matrixDimension, currentPlayer)

                utility, iVal, jVal = alphaBeta(localBoard, gameCell, matrixDimension, moveMaker,
                                                getOpponent(currentPlayer),
                                                depthLimit, currentDepth + 1, alpha, beta)
                # We are in maximiser
                if currentDepth % 2 == 0:
                    if evalValue < utility:
                        evalValue = utility
                    if alpha < utility:

                        # if you are the maximizer node, then you should change the position of the next tile to consider
                        if currentDepth == 0:
                            iTile = i
                            jTile = j
                        if utility < beta:
                            alpha = utility
                        else:
                            prune = True
                            break
                # We are in minimizer
                else:
                    if evalValue > utility:
                        evalValue = utility

                    if beta > utility:
                        if utility > alpha:
                            beta = utility
                        else:
                            prune = True
                            break

    return evalValue, iTile, jTile


def markAndScoreRaidPositions(tempBoard, iNew, jNew, matrixDimension, moveMaker, gameCell):
    opponent = getOpponent(moveMaker)
    moveSum = gameCell[iNew][jNew]
    if isInRange(iNew + 1, jNew, matrixDimension) and tempBoard[iNew + 1][jNew] == opponent:
        tempBoard[iNew + 1][jNew] = moveMaker
        moveSum += gameCell[iNew + 1][jNew]
    if isInRange(iNew - 1, jNew, matrixDimension) and tempBoard[iNew - 1][jNew] == opponent:
        tempBoard[iNew - 1][jNew] = moveMaker
        moveSum += gameCell[iNew - 1][jNew]
    if isInRange(iNew, jNew - 1, matrixDimension) and tempBoard[iNew][jNew - 1] == opponent:
        tempBoard[iNew][jNew - 1] = moveMaker
        moveSum += gameCell[iNew][jNew - 1]
    if isInRange(iNew, jNew + 1, matrixDimension) and tempBoard[iNew][jNew + 1] == opponent:
        tempBoard[iNew][jNew + 1] = moveMaker
        moveSum += gameCell[iNew][jNew + 1]
    return moveSum


def calculateMoveAndBreakTies(boardState, iTile, jTile, matrixDimension, moveMaker, gameCell):
    move = None
    score = None
    iNew = iTile
    jNew = jTile
    tempBoard = copy.deepcopy(boardState)
    tempBoardTie = copy.deepcopy(boardState)
    # if isInRange(iTile, jTile, matrixDimension):
    if isValidStake(tempBoard, iNew, jNew, matrixDimension, moveMaker):
        setPosition(tempBoard, iNew, jNew, moveMaker)
        score = getEvalScore(tempBoard, gameCell, moveMaker, matrixDimension)
        move = 'Stake'
    else:
        # This a raid position
        setPosition(tempBoard, iNew, jNew, moveMaker)
        markRaidPositions(tempBoard, iNew, jNew, matrixDimension, moveMaker)
        score = getEvalScore(tempBoard, gameCell, moveMaker, matrixDimension)
        move = 'Raid'
    # break ties by preferring stakes
    if move == 'Raid':
        for i in range(matrixDimension):
            for j in range(matrixDimension):
                if isPositionEmpty(tempBoardTie, i, j):
                    setPosition(tempBoardTie, i, j, moveMaker)
                    tempScoreForPosition = getEvalScore(tempBoardTie, gameCell, moveMaker, matrixDimension)
                    if score and score == tempScoreForPosition:
                        move = 'Stake'
                        iNew, jNew = i, j
                        break
                    revertPosition(tempBoardTie, i, j, moveMaker)
                    # Now move will have the actual final move after breaking ties and iNew and jNew contains the position that MoveMaker should take
    # setFinalBoardState in the boardState matrix
    if move == 'Stake':
        setPosition(boardState, iNew, jNew, moveMaker)
    else:
        setPosition(boardState, iNew, jNew, moveMaker)
        markRaidPositions(boardState, iNew, jNew, matrixDimension, moveMaker)
    return iNew, jNew, move, boardState


def main():
    inputSpec = []
    gameCell = []
    boardState = []

    with open('input.txt', 'r') as file:
        for line in file:
            inputSpec.append(line.strip())
    if len(inputSpec) > 0:
        matrixDimension = int(inputSpec[0].strip())
        algorithm = inputSpec[1].strip()
        player = inputSpec[2].strip()
        moveMaker = currentPlayer = player
        depth = int(inputSpec[3].strip())
        gameCellIterator = 4
        for row in range(matrixDimension):
            gameCell.append(list(map(int, inputSpec[gameCellIterator + row].split(' '))))
        boardStateIterator = gameCellIterator + matrixDimension
        for row in range(matrixDimension):
            boardState.append(list(inputSpec[boardStateIterator + row]))
        currentDepth = 0
        if algorithm == 'MINIMAX':

            maximizerVal, iTile, jTile = minimax(boardState, gameCell, matrixDimension, moveMaker, currentPlayer, depth,
                                                 currentDepth)
        elif algorithm == 'ALPHABETA':
            maximizerVal, iTile, jTile = alphaBeta(boardState, gameCell, matrixDimension, moveMaker, currentPlayer, depth,
                                                   currentDepth, -math.inf, math.inf)

        iNew, jNew, move, boardState = calculateMoveAndBreakTies(boardState, iTile, jTile, matrixDimension, moveMaker,
                                                                 gameCell)
        state = chr(jNew + 65) + str(iNew + 1) + ' ' + move
        writeOutput('output.txt', state, boardState)
        print(state)
        print(boardState)


if __name__ == '__main__':
    main()
# exec_time = '{:.2f}s'.format(timeit.timeit("main()",
#                                                setup="from __main__ import main", number=1))
# print(exec_time)
