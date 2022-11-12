from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *

def appStarted(app):
    app.margin = min(app.width, app.height)//15
    app.maze = Maze(15)
    app.level = 1
    exitBlockProportion = 0.6
    app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion)
    app.maze.addExit(app.exitBlock)
    app.player = Player(app, app.maze)

def timerFired(app):
    pass

def keyPressed(app, event):
    app.player.keyPressed(app, event)

def redrawAll(app, canvas):
    app.maze.redraw(app, canvas)
    app.exitBlock.redraw(app, canvas)
    app.player.redraw(app, canvas)

runApp(width=1500, height=600)