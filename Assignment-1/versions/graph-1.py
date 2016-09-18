import sys
import queue
from collections import namedtuple

algo = ['BFS', 'DFS', 'UCS', 'A*']


# graphDict
# [
# Node1: [(Node, weight of the edge (Node1->Node), order of the edge)]
# Node2: [(Node, weight of the edge (Node2->Node), order of the edge)]
# ]

# childlist:[(Node, weight of the edge (Node1->Node), order of the edge)]

# priority in the edge is required for the maintaining the input order in case of ties on same path cost

# minPathToNode dictionary 
#  A:[A] 
#  B:[A,B] 
#  C:[A,C] 
#  D:[A,B,D]
#  E:[A,B,E]
#  I:[A,B,D,I]
#  F:[A,B,D,F]

#Edge = namedtuple('Edge', 'child edgecost order')
#-------------------------------- InformedSearch Helpers----------------------------------------------------------
def isNodePresentInQueue(queue, node):
    for priority in queue:
        if priority.node == node:
            return priority
    return None

# childPriority - Priority(pathCost=5, node=Node(D), parent=Node(B)]
# currentParent- Node(C)
# edge-Edge(child=Node(D), edgecost=1, order=3)

def costFunction(oldChild, currentParent, newChild):
    currentCost = newChild.edgecost +  currentParent.pathcost
    oldCost = oldChild.pathcost
    if oldCost > currentCost:
        return Priority(newChild.node, currentCost, currentParent.node)
    return None


def informedSearch(graphObj, startNodeObj, goalNodeObj, costFunction):
    nodeDict = graphObj.graphDict
    open = queue.PriorityQueue()
    closed = dict()
    # insert the start node
    prtuple = Priority(0, startNodeObj, None)
    open.put(prtuple)
    while not open.empty():
        currentNode = open.get()
        if currentNode == goalNodeObj:
            return currentNode
        children = nodeDict[currentNode]
        for edge in children:
            childFromQueue = isNodePresentInQueue(open.queue, edge.child)
            currentParentFromQueue = isNodePresentInQueue(open.queue, currentNode)
            if not childFromQueue and not edge.child in closed:
                prtuple = Priority(edge.edgecost, edge.child, currentNode)
                open.put(prtuple)
            elif childFromQueue:
                newPriority = costFunction(childFromQueue, currentParentFromQueue, edge)
                if newPriority:


                    # the cost is new path is less so replace the child in queue with this new pathcost


        closed[currentNode] = open.get()



#--------------------------------BFS Helpers----------------------------------------------------------
# Returns priority from (Node, weight of the edge (Node1->Node), priority of the edge) of the child
def getEdgePriority(parentchildList, child):
    edgeDetails = [tuple for tuple in parentchildList if tuple.child == child]
    return edgeDetails[0].priority


# Returns weight cost from (Node, weight of the edge (Node1->Node), priority of the edge) of the child
def getEdgeCost(parentchildList, child):
    edgeDetails = [tuple for tuple in parentchildList if tuple.child == child]
    return edgeDetails[0].edgecost

def decidePath(graphDict, oldPath, newPath):
    differingIndex = [i for i, x in enumerate(zip(oldPath, newPath)) if x[0] != x[1]][0]
    differingEdge1 = oldPath[differingIndex - 1: differingIndex + 1]
    differingEdge2 = newPath[differingIndex - 1: differingIndex + 1]
    if getEdgePriority(graphDict[differingEdge1[0]], differingEdge1[1]) < getEdgePriority(graphDict[differingEdge2[0]], differingEdge2[1]):
        return oldPath
    return newPath


def getBFSAccumulatedCost(graphDict, minPathToGoal):
    edgeCost = 0
    pathCost = []
    Route = namedtuple('Route', 'location time')
    initialState = Route(minPathToGoal[0].name, edgeCost)
    pathCost.append(initialState)
    for i in range(len(minPathToGoal) - 1):
        edgeCost += getEdgeCost(graphDict[minPathToGoal[i]], minPathToGoal[i + 1])
        route = Route(minPathToGoal[i + 1].name, edgeCost)
        pathCost.append(route)
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
            return getBFSAccumulatedCost(graphObj.graphDict, resultMinPath)
        else:
            for edge in graphObj.graphDict[nodeObj]:
                if not edge.child in bfsqueue.queue and not visited[edge.child]:
                    bfsqueue.put(edge.child)

                # compare and update path
                newPathList = minPathToNode[nodeObj] + [edge.child] # append two list
                if not minPathToNode[edge.child] or len(minPathToNode[edge.child]) > len(newPathList):
                    minPathToNode[edge.child] = newPathList
                else:
                    if len(minPathToNode[edge.child]) == len(newPathList):
                        minPathToNode[edge.child] = decidePath(graphObj.graphDict, minPathToNode[edge.child], newPathList)

    return resultMinPath  # this contains only path now. I have to fit in the cost
#--------------------------------DFS Helpers----------------------------------------------------------
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
            for edge in graphObj.graphDict[nodeObj]:
                if not edge.child in dfsStack and not visited[edge.child]:
                    dfsStack.append(edge.child)

                # compare and update path
                newPathList = minPathToNode[nodeObj] + [edge.child] # append two list
                if not minPathToNode[edge.child] or len(minPathToNode[edge.child]) > len(newPathList):
                    minPathToNode[edge.child] = newPathList
                else:
                    if len(minPathToNode[edge.child]) == len(newPathList):
                        minPathToNode[edge.child] = decidePath(minPathToNode[edge.child], newPathList)
    return resultMinPath  # this contains only path now. I have to fit in the cost
#--------------------------------Class Definition----------------------------------------------------------
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
    def __init__(self, name, sundayTraffic):
        self.name = name
        self.sundayTraffic = sundayTraffic

    def getName(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

# class Priority(object):
#     def __init__(self, costpriority, node, parent):
#         self.costpriority = costpriority
#         self.node = node
#         self.parent = parent
#
#     def __lt__(self, other):
#         return self.costpriority < other.costpriority
#
#     def __eq__(self, other):
#         return self.costpriority == other.costpriority


# --------------------------------Main Function----------------------------------------------------------
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
    order = 1  # this order is used to break the tie for BFS if multiple paths of same length exists
    hopList = []  # edge with pathcost list
    for i in range(4, hops + index, 1):
        hopList.append(inputSpec[i].strip())
    sundayTrafficIndex = i + 1
    sundayTrafficLines = int(inputSpec[sundayTrafficIndex])

    for j in range(sundayTrafficIndex+1, sundayTrafficIndex + sundayTrafficLines + 1, 1):
        # the sunday traffic gives us detail about the number of nodes
        nodeName, traffic = inputSpec[j].split(' ')
        nodeObj = Node(nodeName.strip(), int(traffic))
        # initialize the graph dictionary for all nodes
        nameToNodeMap[nodeName] = nodeObj
        graphDict[nodeObj] = []

    # update the childlist and edge and the pathcost
    # create a namesTuple to store the edge details
    Edge = namedtuple('Edge', 'child edgecost order')
    #create a namedtuple priority
    Priority = namedtuple('Priority', 'pathcost node parent')
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
            edge = Edge(nameToNodeMap[child], cost, order)
            graphDict[nameToNodeMap[parent]].append(edge)
        order += 1

    # initialize the Graph
    graphObj = Graph(searchType, True, sundayTrafficLines, graphDict)

    if searchType == 'BFS':
        pathCost = bfsIterator(graphObj, nameToNodeMap[startNode], nameToNodeMap[goalNode])
    if searchType == 'UCS':
        pathCost = informedSearch(graphObj, nameToNodeMap[startNode], nameToNodeMap[goalNode], ucsCostFunction)
    if searchType == 'A*':
        pathCost = informedSearch(graphObj, nameToNodeMap[startNode], nameToNodeMap[goalNode], acostFunction)

    print(pathCost)
