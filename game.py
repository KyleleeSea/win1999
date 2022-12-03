# https://hello-tazzina.itch.io/greenwoods-ii Sprites

from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *
from footstepSound import *
from backgroundLogic import *
from enemy import *
from playerShadow import *
from raycaster import *
from splashScreens import *
from sprite import *
import random

class Game:
    def __init__(self):
        # https://hello-tazzina.itch.io/greenwoods-ii
        self.bareTreeSprites = []
        for i in range(1,4):
            imgPath =  f'./assets/bareTree{i}Sprite.png'
            self.bareTreeSprites.append(imgPath)

        self.treeSprites = []
        for i in range(1,7):
            imgPath =  f'./assets/tree{i}Sprite.png'
            self.treeSprites.append(imgPath)
        
        self.otherSprites = ['./assets/statueSprite.png', 
        './assets/cauldronJarsSprite.png', './assets/closetSprite.png', 
        './assets/clothesSprite.png', './assets/runeSprite.png',
        './assets/scarecrowSprite.png', './assets/shelfSprite.png',
         './assets/shopSprite.png', './assets/wellSprite.png',
        './assets/wheelBarrowSprite.png']

    def initSprites(self, app):
        spritesList = [app.enemy.spriteVisual]
        openCells = app.maze.getOpenCells()
        openCells.remove((1,1))
        random.shuffle(openCells)
        for i in range(len(openCells)//4):
            (row, col) = openCells[i]
            randObj = random.randint(1,10)
            # If <= 4 choose tree
            if randObj <= 4:
                ind = random.randint(0, len(self.treeSprites) - 1)
                toAppend = Sprite(self.treeSprites[ind], 16, row, col, app)
            # If >= 4 but <= 8 choose bare tree
            elif randObj > 4 and randObj <= 8:
                ind = random.randint(0, len(self.bareTreeSprites) - 1)
                toAppend = Sprite(self.bareTreeSprites[ind], 16, row, col, app)
            # else choose other
            else:
                ind = random.randint(0, len(self.otherSprites) - 1)
                toAppend = Sprite(self.otherSprites[ind], 16, row, col, app)      
            spritesList.append(toAppend)
        return spritesList

    def startGame(self, app):
        app.cellHeight = 128
        app.cellWidth = 128

        app.wallHeight = (1/3)*app.height
        app.distToPlane = (app.width/2)*math.tan(math.radians(30))

        app.maze = Maze(15) #prev 15
        app.level = 1
        exitBlockProportion = 0.6
        app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion, app)
        app.maze.addExit(app.exitBlock)
        app.player = Player(app, app.maze)
        app.enemy = Enemy(app, app.maze)
        app.playerShadow = PlayerShadow(app)

        # https://obsydianx.itch.io/horror-sfx-volume-1
        app.backgroundSound = footstepSound('./assets/footsteps.mp3') 
        app.collisionSound = Sound('./assets/collision.mp3')

        #Init sprites
        app.sprites = self.initSprites(app)

        app.raycaster = Raycaster(app, app.maze)

        # Player can be in same cell for up to 1 second before dying
        secondsToDie = 1
        mstoDie = secondsToDie*1000
        app.dieIntervals = mstoDie//app.timerDelay
        app.collisionCounter = 0
        app.collisionImage = app.loadImage('./assets/bonziLooking.png')
        app.death = Death(app)

        app.secondsToWin = 0.5*60
        msToWin = app.secondsToWin*1000
        app.winIntervals = msToWin//app.timerDelay
        app.currentWinInterval = 0
        app.timeRemaining = app.secondsToWin
        app.win = Win(app)
        app.exitOpen = False

    def timerFired(self, app):
        # in backgroundLogic
        checkCollision(app)
        if app.exitOpen != True:
            checkTimer(app)
        # app.enemy.timerFired(app)
        app.playerShadow.timerFired(app)

    # def mouseMoved(self, app, event):
    #     app.player.mouseMoved(app, event)

    def keyPressed(self, app, event):
        app.player.keyPressed(app, event)

    def redraw(self, app, canvas):
        app.raycaster.redraw(app, canvas)
        displayTimeLeft(app, canvas)
        
        # Commented out 2d representation debugging code
        app.maze.redraw(app, canvas)
        app.exitBlock.redraw(app, canvas)
        app.player.redraw(app, canvas)
        app.enemy.redraw(app, canvas)
        # in backgroundLogic
        # drawCollision(app, canvas)

    def appStopped(self, app):
        app.backgroundSound.appStopped(app)