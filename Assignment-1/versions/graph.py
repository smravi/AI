import sys
import queue

algo = ['BFS', 'DFS', 'UCS', 'A*']


# graphDict
# [
# Node1: childList
# Node2: childList
# ]

# childlist:[(Node, weight of the edge (Node1->Node), priority of the edge)]

# priority in the edge is required for the maintaining the input order in case of ties on same path cost

# minPathToNode:[([Node1, Node2, Node3, Node4], min cost from Node1 to Node4), ([Node1, Node2, Node5, Node4], min cost from Node1 to Node4)]
# minPathToNode dictionary 
#  A:[A] 
#  B:[A,B] 
#  C:[A,C] 
#  D:[A,B,D]
#  E:[A,B,E]
#  I:[A,B,D,I]
#  F:[A,B,D,F]

def decidePath(oldPath, newPath):
    differingIndex = [i for i, x in enumerate(zip(oldPath, newPath)) if x[0] != x[1]][0]
    differingEdge1 = oldPath[differingIndex - 1: differingIndex + 1]
    differingEdge2 = newPath[differingIndex - 1: differingIndex + 1]
    if differingEdge1[0].getEdgePriority(differingEdge1[1]) < differingEdge2[0].getEdgePriority(differingEdge2[1]):
        return oldPath
    return newPath


def getBFSAccumulatedCost(minPathToGoal):
    edgeCost = 0
    pathCost = []
    pathCost.append((minPathToGoal[0].name, edgeCost))
    for i in range(len(minPathToGoal) - 1):
        edgeCost += minPathToGoal[i].getEdgeCost(minPathToGoal[i + 1])
        pathCost.append((minPathToGoal[i + 1].name, edgeCost))
    return pathCost

def bfsIterator(graphObj, startNodeObj, goalNodeObj):
    bfsqueue = queue.Queue()
    minPathToNode = dict(zip(graphObj.graphDict.keys(), [[]] * len(graphObj.graphDict.keys())))
    visited = dict(zip(graphObj.graphDict.keys(), [False] * len(graphObj.graphDict.keys())))
    resultMinPath = []

    bfsqueue.put(startNodeObj)
    minPathToNode[startNodeObj] = [startNodeObj]
    while not bfsqueue.empty():
        # deque
        nodeObj = bfsqueue.get()
        visited[nodeObj] = True
        if nodeObj == goalNodeObj:
            resultMinPath = minPathToNode[nodeObj]
            return getBFSAccumulatedCost(resultMinPath)
        else:
            for child in nodeObj.childList:
                if not child[0] in bfsqueue.queue and not visited[child[0]]:
                    bfsqueue.put(child[0])

                # compare and update path
                newPathList = minPathToNode[nodeObj] + [child[0]] # append two list
                if not minPathToNode[child[0]] or len(minPathToNode[child[0]]) > len(newPathList):
                    minPathToNode[child[0]] = newPathList
                else:
                    if len(minPathToNode[child[0]]) == len(newPathList):
                        minPathToNode[child[0]] = decidePath(minPathToNode[child[0]], newPathList)

    return resultMinPath  # this contains only path now. I have to fit in the cost

def dfsIterator(graphObj, startNodeObj, goalNodeObj):
    dfsStack = []
    minPathToNode = dict(zip(graphObj.graphDict.keys(), [[]] * len(graphObj.graphDict.keys())))
    visited = dict(zip(graphObj.graphDict.keys(), [False] * len(graphObj.graphDict.keys())))
    resultMinPath = []
    dfsStack.put(startNodeObj)
    minPathToNode[startNodeObj] = [startNodeObj]
    while not dfsStack.empty():
        # deque
        nodeObj = dfsStack.pop()
        visited[nodeObj] = True
        if nodeObj == goalNodeObj:
            resultMinPath = minPathToNode[nodeObj]
            return getBFSAccumulatedCost(resultMinPath)
        else:
            for child in nodeObj.childList:
                if not child[0] in dfsStack and not visited[child[0]]:
                    dfsStack.append(child[0])

                # compare and update path
                newPathList = minPathToNode[nodeObj] + [child[0]] # append two list
                if not minPathToNode[child[0]] or len(minPathToNode[child[0]]) > len(newPathList):
                    minPathToNode[child[0]] = newPathList
                else:
                    if len(minPathToNode[child[0]]) == len(newPathList):
                        minPathToNode[child[0]] = decidePath(minPathToNode[child[0]], newPathList)

    return resultMinPath  # this contains only path now. I have to fit in the cost
class Graph:
    def __init__(self, searchType, isDirected, hops, graphDict):
        self.searchType = searchType
        self.isDirected = isDirected
        self.nodeCount = hops
        self.graphDict = graphDict

    def getGraph(self):
        return self.graphDict

    def getNodeCount(self):
        return self.nodeCount


class Node(object):
    def __init__(self, name, childList, sundayTraffic):
        self.name = name
        self.childList = childList or []
        self.sundayTraffic = sundayTraffic

    def addChild(self, nodeObj, weight, priority):
        self.childList.append((nodeObj, weight, priority))

    def getChildList(self):
        return self.childList

    def getName(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


    # Returns priority from (Node, weight of the edge (Node1->Node), priority of the edge) of the child
    def getEdgePriority(self, child):
        edgeDetails = [tuple for tuple in self.childList if tuple[0] == child]
        return edgeDetails[0][2]

    # Returns weight cost from (Node, weight of the edge (Node1->Node), priority of the edge) of the child
    def getEdgeCost(self, child):
        edgeDetails = [tuple for tuple in self.childList if tuple[0] == child]
        return edgeDetails[0][1]


# gets the input from the file and normalizes the input

inputSpec = []
graphDict = dict()
nameToNodeMap = dict()
with open('input1.txt', 'r') as file:
    for line in file:
        inputSpec.append(line.strip())
if len(inputSpec) > 0:
    searchType = inputSpec[0]
    startNode = inputSpec[1].strip()
    goalNode = inputSpec[2].strip()
    hops = int(inputSpec[3])
    index = 4  # this is the start index where the list of routes are specified
    priority = 1  # this priority is used to break the tie for BFS if multiple paths of same length exists
    hopList = []  # edge with pathcost list
    for i in range(4, hops + index, 1):
        hopList.append(inputSpec[i].strip())
    sundayTrafficIndex = i + 1
    sundayTrafficLines = int(inputSpec[sundayTrafficIndex])

    for j in range(sundayTrafficIndex+1, sundayTrafficIndex + sundayTrafficLines + 1, 1):
        # the sunday traffic gives us detail about the number of nodes
        nodeName, traffic = inputSpec[j].split(' ')
        nodeObj = Node(nodeName.strip(), [], int(traffic))
        # initialize the graph dictionary for all nodes
        nameToNodeMap[nodeName] = nodeObj
        graphDict[nodeObj] = []

    # update the childlist and edge and the pathcost
    for hop in hopList:
        parent, child, cost = hop.split(' ')
        parent = parent.strip()
        child = child.strip()
        cost = cost.strip()
        if nameToNodeMap[parent] in graphDict:
            if searchType == 'BFS' or searchType == 'DFS':
                cost = 1
            else:
                cost = int(cost)
            graphDict[nameToNodeMap[parent]].append((nameToNodeMap[child], cost, priority))
            nameToNodeMap[parent].addChild(nameToNodeMap[child], cost, priority)
        priority += 1

    # initialize the Graph
    graphObj = Graph(searchType, True, sundayTrafficLines, graphDict)

    if searchType == 'BFS':
        pathCost = bfsIterator(graphObj, nameToNodeMap[startNode], nameToNodeMap[goalNode])

    print(pathCost)
