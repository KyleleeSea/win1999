from cmu_112_graphics import *
from maze import *
from exitBlock import *

def appStarted(app):
    app.margin = min(app.width, app.height)//15
    app.maze = Maze(20)
    exitBlockProportion = 0.6
    app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion)

def timerFired(app):
    pass

def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    app.maze.redraw(app, canvas)
    app.exitBlock.redraw(app, canvas)

runApp(width=1920, height=1080)