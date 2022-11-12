from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *

def appStarted(app):
    app.margin = min(app.width, app.height)//15
    app.maze = Maze(20)
    exitBlockProportion = 0.6
    app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion)
    app.player = Player(app, app.maze)

def timerFired(app):
    # app.player.timerFired(app)
    pass

def keyPressed(app, event):
    app.player.keyPressed(app, event)

def redrawAll(app, canvas):
    app.maze.redraw(app, canvas)
    app.exitBlock.redraw(app, canvas)
    app.player.redraw(app, canvas)

runApp(width=1920, height=1080)