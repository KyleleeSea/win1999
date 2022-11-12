from cmu_112_graphics import *
from helpers import *
import random

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = self.generateMaze(size)

    def generateMaze(self, size):
        maze2D = generate2DList(size)
        protectedCells = getProtectedCells(maze2D)
        # Break starting wall and initialize variables
        maze2D[1][1] = 0
        openCellsList = [(1,1)]

        return mazeBacktracker(maze2D, protectedCells, openCellsList)

    def redraw(self, app, canvas):
        for rowIndex in range(len(self.maze)):
            for colIndex in range(len(self.maze[rowIndex])):
                if self.maze[rowIndex][colIndex] == 1:
                    drawWall(app, canvas, rowIndex, colIndex, self.maze)
                else:
                    drawOpen(app, canvas, rowIndex, colIndex, self.maze)

#--------------------------
# Maze Generation Helpers
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

def mazeIsFinished(maze, openCellsList, finishCondition):
    if maze == None:
        return False
    else:
        totalCells = len(maze)**2
        if len(openCellsList) >= totalCells*finishCondition:
            return True
        return False

def notMiddle(maze, newRow, newCol):
    (rows, cols) = (len(maze), len(maze[0]))
    if ((newRow+1) > rows or (newRow-1) < 0 or maze[newRow+1][newCol] == 1 or
    maze[newRow-1][newCol] == 1):
        if ((newCol+1) > cols or (newCol-1) < 0 or maze[newRow][newCol+1] == 1 
        or maze[newRow][newCol-1] == 1):
            return True
    return False

def isLegal(maze, newRow, newCol, protectedCells):
    (rows, cols) = (len(maze), len(maze[0]))
    if newRow < rows and newRow >= 0 and newCol < cols and newCol >= 0:
        if (newRow, newCol) not in protectedCells:
            if maze[newRow][newCol] == 1:
                if notMiddle(maze, newRow, newCol):
                    return True
    return False

# https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#Backtracking 
# nQueens ^. Also recitation Nov 9th
def mazeBacktracker(maze, protectedCells, openCellsList):
    finishCondition = 0.5
    if mazeIsFinished(maze, openCellsList, finishCondition):
        return maze
    else:
        # https://www.w3schools.com/python/ref_random_shuffle.asp
        # Set up Moves

        moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        random.shuffle(moves)
        # Loop through "moves" (both all cells and all move states)
        for openCell in openCellsList:
            for move in moves:
                (currRow, currCol) = openCell
                (adjRow, adjCol) = move
                (newRow, newCol) = (currRow+adjRow, currCol+adjCol)
                # Check legality
                if isLegal(maze, newRow, newCol, protectedCells):
                    maze[newRow][newCol] = 0
                    # openCellsList.insert(0, (newRow, newCol))
                    random.shuffle(openCellsList)
                    openCellsList.insert(0, (newRow, newCol))
                    newMaze = mazeBacktracker(maze, protectedCells, 
                    openCellsList)
                    if newMaze != None:
                        return newMaze
                # Undo move
                # https://www.programiz.com/python-programming/methods
                # /list/remove
                #https://www.programiz.com/python-programming/methods/set/remove
                    if (newRow, newCol) in openCellsList: 
                        maze[newRow][newCol] = 1
                        openCellsList.remove((newRow, newCol))
        return None

#----------------------
# Maze drawing helpers
def drawWall(app, canvas, row, col, maze):
    (x0, y0, x1, y1) = getCellBounds(row, col, maze, app)
    canvas.create_rectangle(x0, y0, x1, y1, fill='black')

def drawOpen(app, canvas, row, col, maze):
    (x0, y0, x1, y1) = getCellBounds(row, col, maze, app)
    canvas.create_rectangle(x0, y0, x1, y1, fill='white', outline='black')
