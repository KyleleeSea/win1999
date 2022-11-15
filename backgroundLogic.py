from cmu_112_graphics import *
from maze import *
from player import *
from exitBlock import *
from helpers import *
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
