import queue

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
