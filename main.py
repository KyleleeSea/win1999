from cmu_112_graphics import *
from maze import *

def appStarted(app):
    app.maze = Maze(20)
    app.margin = min(app.width, app.height)//15

def timerFired(app):
    pass

def keyPressed(app, event):
    pass

def redrawAll(app, canvas):
    app.maze.redraw(app, canvas)

runApp(width=1920, height=1080)