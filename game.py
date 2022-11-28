from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *
from backgroundSound import *
from backgroundLogic import *
from enemy import *
from playerShadow import *
from raycaster import *
from death import *

class Game:
    def __init__(self):
        pass

    def startGame(self, app):
        app.cellHeight = 128
        app.cellWidth = 128

        app.wallHeight = (1/6)*app.height
        app.distToPlane = (app.width/2)*math.tan(math.radians(30))

        app.timerDelay = 150
        app.maze = Maze(20)
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

        # Player can be in same cell for up to 2 seconds before dying
        secondsToDie = 1
        mstoDie = secondsToDie*1000
        app.dieIntervals = mstoDie//app.timerDelay
        app.collisionCounter = 0
        app.collisionImage = app.loadImage('./assets/bonziLooking.png')
        app.death = Death(app)

    def timerFired(self, app):
        # in backgroundLogic
        checkCollision(app)
        app.enemy.timerFired(app)
        app.playerShadow.timerFired(app)

    def mouseMoved(self, app, event):
        app.player.mouseMoved(app, event)

    def keyPressed(self, app, event):
        app.player.keyPressed(app, event)

    def redraw(self, app, canvas):
        app.raycaster.redraw(app, canvas)

        app.maze.redraw(app, canvas)
        # app.exitBlock.redraw(app, canvas)
        app.player.redraw(app, canvas)
        app.enemy.redraw(app, canvas)
        # in backgroundLogic
        drawCollision(app, canvas)

    def appStopped(self, app):
        app.backgroundSound.appStopped(app)