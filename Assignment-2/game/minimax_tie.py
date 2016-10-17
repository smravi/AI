import sys

import copy
import timeit
from collections import namedtuple

NextMove = namedtuple('nextMove', 'iIndex, jIndex moveType')

def writeOutput(fileName, state, playerBoard):
    with open(fileName, 'w') as f:
        f.write('{}\n'.format(state))
        for i, row in enumerate(playerBoard):
            for j, col in enumerate(row):
                f.write(playerBoard[i][j])
            f.write('\n')
            # f.truncate(f.tell() - 1)


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


def setPosition(board, i, j, player):
    if isPositionEmpty(board, i, j):
        board[i][j] = player


def revertPosition(board, i, j, player):
    if board[i][j] == player:
        board[i][j] = '.'


def getStakeScore(gameCell, i, j):
    return gameCell[i][j]


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


def markRaidPositions(playerBoard, i, j, matrixDimension, currentPlayer):
    opponent = getOpponent(currentPlayer)
    markedPositions = []
    if isInRange(i, j - 1, matrixDimension) and playerBoard[i][j - 1] == opponent:
        playerBoard[i][j - 1] = currentPlayer
        markedPositions.append((i, j - 1))
    if isInRange(i, j + 1, matrixDimension) and playerBoard[i][j + 1] == opponent:
        playerBoard[i][j + 1] = currentPlayer
        markedPositions.append((i, j + 1))
    if isInRange(i + 1, j, matrixDimension) and playerBoard[i + 1][j] == opponent:
        playerBoard[i + 1][j] = currentPlayer
        markedPositions.append((i + 1, j))
    if isInRange(i - 1, j, matrixDimension) and playerBoard[i - 1][j] == opponent:
        playerBoard[i - 1][j] = currentPlayer
        markedPositions.append((i - 1, j))
    return markedPositions


def calculateMoveAndBreakTies(playerBoard, iTile, jTile, matrixDimension, moveMaker, gameCell, moveFromAlgo):
    print(moveFromAlgo)
    score = None
    finalMove = None
    iNew = iTile
    jNew = jTile
    tempBoard = copy.deepcopy(playerBoard)
    tempBoardTie = copy.deepcopy(playerBoard)
    if moveFromAlgo and moveFromAlgo.moveType:
        finalMove = moveFromAlgo.moveType
    # # if isInRange(iTile, jTile, matrixDimension):
    # if isValidStake(tempBoard, iNew, jNew, matrixDimension, moveMaker):
    #     setPosition(tempBoard, iNew, jNew, moveMaker)
    #     score = getEvalScore(tempBoard, gameCell, moveMaker, matrixDimension)
    #     move = 'Stake'
    # else:
    #     # This a raid position
    #     setPosition(tempBoard, iNew, jNew, moveMaker)
    #     markRaidPositions(tempBoard, iNew, jNew, matrixDimension, moveMaker)
    #     score = getEvalScore(tempBoard, gameCell, moveMaker, matrixDimension)
    #     move = 'Raid'
    # # break ties by preferring stakes
    if finalMove == 'Raid':
        setPosition(tempBoard, iNew, jNew, moveMaker)
        markRaidPositions(tempBoard, iNew, jNew, matrixDimension, moveMaker)
        score = getEvalScore(tempBoard, gameCell, moveMaker, matrixDimension)
        stakeFound = False
        for i in range(matrixDimension):
            if stakeFound:
                break
            for j in range(matrixDimension):
                if isPositionEmpty(tempBoardTie, i, j):
                    setPosition(tempBoardTie, i, j, moveMaker)
                    tempScoreForPosition = getEvalScore(tempBoardTie, gameCell, moveMaker, matrixDimension)
                    if score and score == tempScoreForPosition:
                        finalMove = 'Stake'
                        iNew, jNew = i, j
                        stakeFound = True
                        break
                    revertPosition(tempBoardTie, i, j, moveMaker)
                    # Now move will have the actual final move after breaking ties and iNew and jNew contains the position that MoveMaker should take
    # setFinalplayerBoard in the playerBoard matrix
    if finalMove == 'Stake':
        setPosition(playerBoard, iNew, jNew, moveMaker)
    else:
        setPosition(playerBoard, iNew, jNew, moveMaker)
        markRaidPositions(playerBoard, iNew, jNew, matrixDimension, moveMaker)
    return iNew, jNew, finalMove, playerBoard


def minimax(playerBoard, gameCell, matrixDimension, moveMaker, currentPlayer, depthLimit, currentDepth, opteval):
    iTile = -1
    jTile = -1
    minimaxMove = None
    if currentDepth % 2 == 0:
        evalValue = -float("inf")
    else:
        evalValue = float("inf")

    # break recursion
    if isBoardComplete(playerBoard, matrixDimension) or currentDepth == depthLimit:
        # evalValue = getEvalScore(playerBoard, gameCell, moveMaker, matrixDimension)
        evalValue = opteval
        return evalValue, iTile, jTile, minimaxMove
    # maximizer is in position 0,2,4

    for i in range(matrixDimension):
        for j in range(matrixDimension):
            if isPositionEmpty(playerBoard, i, j):
                moveList = []
                moveList.append(NextMove(i, j, 'Stake'))
                if not isValidStake(playerBoard, i, j, matrixDimension, currentPlayer):
                    moveList.append(NextMove(i, j, 'Raid'))
                for moveEntry in moveList:
                    localBoard = [row[:] for row in playerBoard]
                    if moveEntry.moveType == 'Stake':
                        localBoard[i][j] = currentPlayer
                        moveVal = gameCell[i][j]
                    else:
                        localBoard[i][j] = currentPlayer
                        markedPositions = markRaidPositions(localBoard, i, j, matrixDimension, currentPlayer)
                        opponentVal = gameCell[i][j]
                        moveVal = 0
                        for position in markedPositions:
                            opponentVal += gameCell[position[0]][position[1]]
                        previousPlayerVal = opponentVal - gameCell[i][j]
                        moveVal = opponentVal + previousPlayerVal
                    # call minimiax
                    if currentPlayer == moveMaker:
                        utility, miniX, miniY, moveWaste = minimax(localBoard, gameCell, matrixDimension, moveMaker,
                                                        getOpponent(currentPlayer),
                                                        depthLimit, currentDepth + 1, opteval + moveVal)
                    else:
                        utility, miniX, miniY, moveWaste = minimax(localBoard, gameCell, matrixDimension, moveMaker,
                                                        getOpponent(currentPlayer),
                                                        depthLimit, currentDepth + 1, opteval - moveVal)
                    # We are in maximiser
                    if currentDepth % 2 == 0:
                        #                    if utility > evalValue and utility > alpha:
                        if utility > evalValue:
                            evalValue = utility
                            # if you are the maximizer node, then you should change the position of the next tile to consider
                            if currentDepth == 0:
                                iTile = i
                                jTile = j
                                minimaxMove = moveEntry
                    # We are in minimizer
                    else:
                        #                    if utility < evalValue and utility < beta:
                        if utility < evalValue:
                            evalValue = utility

    return evalValue, iTile, jTile, minimaxMove


def alphaBeta(playerBoard, gameCell, matrixDimension, moveMaker, currentPlayer, depthLimit, currentDepth, alpha, beta,
              opteval):
    iTile = -1
    jTile = -1
    alphabetaMove = None
    if currentDepth % 2 == 0:
        evalValue = -float("inf")
    else:
        evalValue = float("inf")

    # break recursion
    if isBoardComplete(playerBoard, matrixDimension) or currentDepth == depthLimit:
        # evalValue = getEvalScore(playerBoard, gameCell, moveMaker, matrixDimension)
        evalValue = opteval
        return evalValue, iTile, jTile, alphabetaMove
    # maximizer is in position 0,2,4
    #prune = False
    for i in range(matrixDimension):
        # if prune:
        #     break
        for j in range(matrixDimension):
            if isPositionEmpty(playerBoard, i, j):
                moveList = []
                moveList.append(NextMove(i, j, 'Stake'))
                if not isValidStake(playerBoard, i, j, matrixDimension, currentPlayer):
                    moveList.append(NextMove(i, j, 'Raid'))
                for moveEntry in moveList:
                    localBoard = [row[:] for row in playerBoard]
                    if moveEntry.moveType == 'Stake':
                        localBoard[i][j] = currentPlayer
                        moveVal = gameCell[i][j]
                    else:
                        localBoard[i][j] = currentPlayer
                        markedPositions = markRaidPositions(localBoard, i, j, matrixDimension, currentPlayer)
                        opponentVal = gameCell[i][j]
                        moveVal = 0
                        for position in markedPositions:
                            opponentVal += gameCell[position[0]][position[1]]
                        previousPlayerVal = opponentVal - gameCell[i][j]
                        moveVal = opponentVal + previousPlayerVal
                    # call minimiax
                    if currentPlayer == moveMaker:
                        utility, alphaX, alphaY, moveWaste = alphaBeta(localBoard, gameCell, matrixDimension, moveMaker,
                                                                   getOpponent(currentPlayer),
                                                                   depthLimit, currentDepth + 1, alpha, beta, opteval + moveVal)
                    else:
                        utility, alphaX, alphaY, moveWaste = alphaBeta(localBoard, gameCell, matrixDimension, moveMaker,
                                                                   getOpponent(currentPlayer),
                                                                   depthLimit, currentDepth + 1, alpha, beta, opteval - moveVal)
                # We are in maximiser
                    if currentDepth % 2 == 0:
                        if evalValue < utility:
                            evalValue = utility
                        if alpha < utility:

                            # if you are the maximizer node, then you should change the position of the next tile to consider
                            if currentDepth == 0:
                                iTile = i
                                jTile = j
                                alphabetaMove = moveEntry
                            if utility < beta:
                                alpha = utility
                            else:
                                return evalValue, iTile, jTile, alphabetaMove
                                # prune = True
                                # break
                    # We are in minimizer
                    else:
                        if evalValue > utility:
                            evalValue = utility

                        if beta > utility:
                            if utility > alpha:
                                beta = utility
                            else:
                                return evalValue, iTile, jTile, alphabetaMove
                                # prune = True
                                # break

    return evalValue, iTile, jTile, alphabetaMove


def main(inputFile, outputFile):
    # inputFile = input()
    # outputFile = input()

    inputSpec = []
    gameCell = []
    playerBoard = []

    with open(inputFile, 'r') as file:
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
        playerBoardIterator = gameCellIterator + matrixDimension
        for row in range(matrixDimension):
            playerBoard.append(list(inputSpec[playerBoardIterator + row]))
        currentDepth = 0
        initialScore = getEvalScore(playerBoard, gameCell, moveMaker, matrixDimension)
        if algorithm == 'MINIMAX':

            maximizerVal, iTile, jTile, moveReturned = minimax(playerBoard, gameCell, matrixDimension, moveMaker, currentPlayer,
                                                 depth,
                                                 currentDepth, initialScore)

        elif algorithm == 'ALPHABETA':
            maximizerVal, iTile, jTile, moveReturned = alphaBeta(playerBoard, gameCell, matrixDimension, moveMaker, currentPlayer,
                                                   depth,
                                                   currentDepth, -float("inf"), float("inf"), initialScore)

        iNew, jNew, move, playerBoard = calculateMoveAndBreakTies(playerBoard, iTile, jTile, matrixDimension, moveMaker,
                                                                  gameCell, moveReturned)
        state = chr(jNew + 65) + str(iNew + 1) + ' ' + move
        writeOutput(outputFile, state, playerBoard)
        # print(globalInc)
        # print(state)
        # print(playerBoard)


if __name__ == '__main__':
    # main()
    exec_time = '{:.2f}s'.format(timeit.timeit("main('../input/input31.txt', 'dev-test-output/output31.txt')",
                                               setup="from __main__ import main", number=1))
    print(exec_time)
