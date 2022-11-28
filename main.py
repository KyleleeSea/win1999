from game import *
from startScreen import *
from instructions import *

def appStarted(app):
    app.mode = 'start'
    app.start = StartScreen(app)
    # app.game initialized upon starting in start screen
  
# Start screen 
def start_redrawAll(app, canvas):
    app.start.redraw(app, canvas)

def start_keyPressed(app, event):
    app.start.keyPressed(app, event)

# Instructions screen

def instructions_redrawAll(app, canvas):
    app.death.redraw(app, canvas)

def instructions_keyPressed(app, event):
    app.death.keyPressed(app, event)

# Death screen
# app.death initialized in game
def death_redrawAll(app, canvas):
    app.death.redraw(app, canvas)

def death_keyPressed(app, event):
    app.death.keyPressed(app, event)

# Game screen
def game_timerFired(app):
    app.game.timerFired(app)

def game_mouseMoved(app, event):
    app.game.mouseMoved(app, event)

def game_keyPressed(app, event):
    app.game.keyPressed(app, event)

def game_redrawAll(app, canvas):
    app.game.redraw(app, canvas)

def game_appStopped(app):
    app.game.appStopped(app)

runApp(width=1500, height=900)