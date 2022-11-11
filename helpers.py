import random
# Maze Helpers

def generate2DList(size):
    # https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
    return [([1]*size) for row in range(size)]

def getProtectedCells(maze):
    (rows, cols) = (len(maze), len(maze[0]))
    protectedCells = set()
    # Add in (row, col) order
    # Add top and bottom cells
    for i in range(cols):
        protectedCells.add((0, i))
        protectedCells.add((rows - 1, i))
    # Add left and right cells
    for i in range(rows):
        protectedCells.add((i, 0))
        protectedCells.add((i, cols - 1))
    return protectedCells

def mazeIsFinished(maze, openCellsList, proportion):
    if maze == None:
        return False
    else:
        totalCells = len(maze)**2
        print(len(openCellsList))
        print(totalCells*proportion)
        if len(openCellsList) >= totalCells*proportion:
            return True
        return False

def isLegal(maze, newRow, newCol, protectedCells):
    (rows, cols) = (len(maze), len(maze[0]))
    if newRow < rows and newRow >= 0 and newCol < cols and newCol >= 0:
        if (newRow, newCol) not in protectedCells:
            if maze[newRow][newCol] == 1:
                return True
    return False

def changeMazeTile(maze, protectedCells, openCellsList):
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    random.shuffle(moves)
    for openCell in openCellsList:
        for move in moves:
            (currRow, currCol) = openCell
            (adjRow, adjCol) = move
            (newRow, newCol) = (currRow+adjRow, currCol+adjCol)
            if isLegal(maze, newRow, newCol, protectedCells):
                maze[newRow][newCol] = 0
# https://www.programiz.com/python-programming/methods/list/insert
                random.shuffle(openCellsList)
                openCellsList.insert(0, (newRow, newCol))
                return


# https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#Backtracking 
# nQueens ^. Also recitation Nov 9th
def mazeBacktracker(maze, protectedCells, openCellsList, openCellsSet):
    if mazeIsFinished(maze, openCellsList, 0.3):
        return maze
    else:
        # https://www.w3schools.com/python/ref_random_shuffle.asp
        # Set up Moves
        for row in maze:
            print(row)
        print('-----')

        random.shuffle(openCellsList)
        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)
        # Loop through "moves" (both all cells and all move states)
        for openCell in openCellsList:
            for move in moves:
                (currRow, currCol) = openCell
                (adjRow, adjCol) = move
                (newRow, newCol) = (currRow+adjRow, currCol+adjCol)
                # Check legality
                if isLegal(maze, newRow, newCol, protectedCells, openCellsSet):
                    maze[newRow][newCol] = 0
                    openCellsList.append((newRow, newCol))
                    openCellsSet.add((newRow, newCol))
                    newMaze = mazeBacktracker(maze, protectedCells, 
                    openCellsList, openCellsSet)
                    if newMaze != None:
                        return newMaze
                # Undo move
                # https://www.programiz.com/python-programming/methods
                # /list/remove
                #https://www.programiz.com/python-programming/methods/set/remove
                if (newRow, newCol) in openCellsSet: 
                    maze[newRow][newCol] = 1
                    openCellsList.remove((newRow, newCol))
                    openCellsSet.remove((newRow, newCol))
        return None