# https://brilliant.org/wiki/a-star-search/
# https://isaaccomputerscience.org/concepts/dsa_search_a_star
# https://www.youtube.com/watch?v=-L-WgKMFuhE

def manhattanDist(node, app, target):
    nodeRow, nodeCol = node
    targetRow, targetCol = target
    return (abs(targetRow*10 - nodeRow*10) 
    + abs(targetCol*10 - nodeCol*10))

def getShortestPath(endNode, app):
    returnList = []
    currentNode = endNode
    while currentNode['prev'] != None:
        returnList.append(currentNode['coords'])
        currentNode = currentNode['prev']
    app.shortestPath = returnList
    return returnList

def lowestCostNode(nodes):
    best = float('infinity')
    bestNode = None
    for node in nodes:
        if node['f'] < best:
            best = node['f']
            bestNode = node
    return bestNode

def getNeighbors(node):
    neighbors = []
    moves = [(0,1), (0,-1),(1,0),(-1,0)]
    row, col = node['coords']
    for move in moves:
        rowAdj, colAdj = move
        neighbors.append((row+rowAdj, col+colAdj))
    return neighbors

def checkLegal(coords, app):
    row, col = coords
    # Check on board
    if (row < 0 or row >= len(app.maze.maze) or col < 0 or 
    col >= len(app.maze.maze)):
        return False
    # Check if cell is wall
    if app.maze.maze[row][col] == 1:
        return False
    return True

def checkNotInList(neighbor, nodes):
    for node in nodes:
        if neighbor == node['coords']:
            return False
    return True

# target should be player pos 
def shortestPath(startingNode, app, target):
    openNodes = []
    closedNodes = []
    openNodes.append({'coords': startingNode, 'g': 0, 
    'h': manhattanDist(startingNode, app, target),
    'f': manhattanDist(startingNode, app, target),
    'prev': None})

    while True:
        current = lowestCostNode(openNodes)
        openNodes.remove(current)
        closedNodes.append(current)

        if current['coords'] == target:
            return getShortestPath(current, app)

        neighbors = getNeighbors(current)
        for neighbor in neighbors:
            if (checkLegal(neighbor, app) and 
            checkNotInList(neighbor, closedNodes)):
                if checkNotInList(neighbor, openNodes):
                    hCost = manhattanDist(neighbor, app, (app.player.row, 
                    app.player.col))
                    gCost = manhattanDist(neighbor, app, startingNode)
                    fCost = hCost + gCost
                    parent = current
                    openNodes.append({'coords': neighbor,
                    'g': gCost, 'h': hCost, 'f': fCost, 
                    'prev': parent})