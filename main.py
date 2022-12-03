from game import *
from splashScreens import *
from startScreen import *
from soundClass import *
import sys
#https://www.geeksforgeeks.org/python-handling-recursion-limit/
sys.setrecursionlimit(10**6)

def appStarted(app):
    app.timerDelay = 150
    app.mode = 'start'
    app.start = StartScreen(app)
    app.shortestPath = []
    # app.game initialized upon starting in start screen

    #Init audio
    #https://www.pygame.org/docs/ref/mixer.html#pygame.mixer
    pygame.mixer.init()
    pygame.mixer.set_num_channels(8)
    # https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.fadeout
    pygame.mixer.fadeout(3)
    
    # Ambience sound
    # https://www.youtube.com/watch?v=1nD3Sp_saz4
    app.ambientSound = Sound('./assets/ambience.mp3')
    app.ambientSound.start(-1)

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

# def game_mouseMoved(app, event):
#     app.game.mouseMoved(app, event)

def game_keyPressed(app, event):
    app.game.keyPressed(app, event)

def game_redrawAll(app, canvas):
    app.game.redraw(app, canvas)

def appStopped(app):
    app.game.appStopped(app)
    pygame.mixer.stop()

runApp(width=1500, height=700)