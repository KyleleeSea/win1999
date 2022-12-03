from cmu_112_graphics import *
from helpers import *
import random
from sprite import *

class exitBlock:
    def __init__(self, maze, proportion, app):
        self.maze = maze
        self.proportion = proportion
        (self.row, self.col) = createExitCoords(self.maze, self.proportion)

        (x0, y0, x1, y1) = getCellBounds(self.row, self.col, self.maze, app)
        self.xPos = (x1 + x0)//2
        self.yPos = (y1 + y0)//2

        self.spriteRepresentation = Sprite('./assets/exitSprite.png', 64,
        self.row, self.col, app)
    
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = getCellBounds(self.row, self.col, self.maze, app)
        canvas.create_oval(x0//7, y0//7, x1//7, y1//7, fill='green')

        if app.exitOpen:
            self.spriteRepresentation.redraw(app, canvas)

def createExitCoords(maze, proportion):
    (rows, cols) = (len(maze), len(maze[0]))
    topRowBound = int(rows*proportion)
    leftColBound = int(cols*proportion)
    bottomRowBound = rows-2
    rightColBound = cols-2

    while True:
        # https://www.w3schools.com/python/ref_random_randint.asp
        row = random.randint(topRowBound, bottomRowBound)
        col = random.randint(leftColBound, rightColBound)
        if maze[row][col] == 0:
            return (row, col)