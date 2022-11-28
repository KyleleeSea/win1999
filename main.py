from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *
from backgroundSound import *
from enemy import *
from playerShadow import *
from raycaster import *

def appStarted(app):
    app.wallHeight = (1/6)*app.height
    app.distToPlane = (app.width/2)*math.tan(math.radians(30))
    app.enemyIsVisible = True

    app.timerDelay = 100
    app.maze = Maze(10)
    app.level = 1
    exitBlockProportion = 0.6
    app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion, app)
    app.maze.addExit(app.exitBlock)
    app.player = Player(app, app.maze)
    app.enemy = Enemy(app, app.maze)
    app.playerShadow = PlayerShadow(app)

    #Init audio
    pygame.mixer.init()
    # https://obsydianx.itch.io/horror-sfx-volume-1
    app.backgroundSound = backgroundSound('./assets/backgroundAudio.mp3')    

    app.raycaster = Raycaster(app, app.maze)

def timerFired(app):
    app.enemy.timerFired(app)
    app.playerShadow.timerFired(app)

def mouseMoved(app, event):
    app.player.mouseMoved(app, event)

def keyPressed(app, event):
    app.player.keyPressed(app, event)

def redrawAll(app, canvas):
    app.raycaster.redraw(app, canvas)

    app.maze.redraw(app, canvas)
    app.exitBlock.redraw(app, canvas)
    app.player.redraw(app, canvas)
    app.enemy.redraw(app, canvas)

def appStopped(app):
    app.backgroundSound.appStopped(app)

runApp(width=1500, height=600)