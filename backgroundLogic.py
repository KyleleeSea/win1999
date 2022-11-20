from cmu_112_graphics import *
from maze import *
from player import *
from exitBlock import *
from helpers import *
from enemy import *
from playerShadow import *
import pygame

def nextLevel(app):
    app.level += 1
    #Reset maze
    app.maze = Maze(15)
    #Reset exit block
    exitBlockProportion = 0.6
    app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion, app)
    app.maze.addExit(app.exitBlock)

    #Reset player 
    (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, app.maze.maze, 
        app)
    app.player.xPos = int((startX0 + startX1)//2)
    app.player.yPos = int((startY0 + startY1)//2)
    app.player.maze = app.maze.maze
    app.player.exitBlock = app.exitBlock
    app.playerShadow = PlayerShadow(app)

    #Reset enemy
    app.enemy = Enemy(app, app.maze)

def checkLegalMove(lastCol,lastRow, newX, newY, maze, app):
    (row, col) = getCell(app, newX, newY, maze)
    # Checking diagonals
    # Only run check if moving diagonally, otherwise bugs.
    if row-lastRow != 0 and col-lastCol!= 0:
        if maze[lastRow][lastCol + 1] == 1 and maze[row][col-1] == 1:
            return False
        elif maze[lastRow][lastCol-1] == 1 and maze[row][col+1] == 1:
            return False
    # Check cell open
    if maze[row][col] == 0:
        return True
    return False