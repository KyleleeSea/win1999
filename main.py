from game import *
from splashScreens import *
from startScreen import *

def appStarted(app):
    app.timerDelay = 150
    app.mode = 'start'
    app.start = StartScreen(app)
    app.shortestPath = []
    # app.game initialized upon starting in start screen

# Start screen 
def start_redrawAll(app, canvas):
    app.start.redraw(app, canvas)

def start_keyPressed(app, event):
    app.start.keyPressed(app, event)

# Instructions screen
def instructions_redrawAll(app, canvas):
    app.instructions.redraw(app, canvas)

def instructions_keyPressed(app, event):
    app.instructions.keyPressed(app, event)

# Death screen
# app.death initialized in game
def death_redrawAll(app, canvas):
    app.death.redraw(app, canvas)

def death_keyPressed(app, event):
    app.death.keyPressed(app, event)

# Win screen
# app.win initialized in game
def win_redrawAll(app, canvas):
    app.win.redraw(app, canvas)

def win_keyPressed(app, event):
    app.win.keyPressed(app, event)
    
# Game screen
def game_timerFired(app):
    app.game.timerFired(app)

def game_mouseMoved(app, event):
    app.game.mouseMoved(app, event)

def game_keyPressed(app, event):
    app.game.keyPressed(app, event)

def game_redrawAll(app, canvas):
    app.game.redraw(app, canvas)

def appStopped(app):
    app.game.appStopped(app)

runApp(width=1500, height=700)