# https://hello-tazzina.itch.io/greenwoods-ii Sprites

from cmu_112_graphics import *
from maze import *
from exitBlock import *
from player import *
from dynamicSound import *
from backgroundLogic import *
from enemy import *
from playerShadow import *
from raycaster import *
from splashScreens import *
from sprite import *
import random
import time

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
        './assets/clothesSprite.png',
        './assets/scarecrowSprite.png', './assets/shelfSprite.png',
         './assets/shopSprite.png', './assets/wellSprite.png',
        './assets/wheelBarrowSprite.png']

        self.playingLegalSound = False
        self.playingDoorSound = False

    def initSprites(self, app):
        spritesList = [app.enemy.spriteVisual]
        openCells = app.maze.getOpenCells()
        openCells.remove((1,1))
        random.shuffle(openCells)
        for i in range(len(openCells)//2):
            (row, col) = openCells[i]
            randObj = random.randint(1,10)
            # If <= 4 choose tree
            if randObj <= 4:
                ind = random.randint(0, len(self.treeSprites) - 1)
                toAppend = Sprite(self.treeSprites[ind], 16, row, col, app)
            # If >= 4 but <= 8 choose bare tree
            elif randObj > 4 and randObj <= 7:
                ind = random.randint(0, len(self.bareTreeSprites) - 1)
                toAppend = Sprite(self.bareTreeSprites[ind], 16, row, col, app)
            # else choose other
            else:
                ind = random.randint(0, len(self.otherSprites) - 1)
                toAppend = Sprite(self.otherSprites[ind], 16, row, col, app)      
            spritesList.append(toAppend)
        return spritesList

    def startGame(self, app):
        app.timerDelay = 100
        app.cellHeight = 128
        app.cellWidth = 128

        app.wallHeight = (1/3)*app.height
        app.distToPlane = (app.width/2)*math.tan(math.radians(30))

        app.maze = Maze(15) #prev 15 # end game like size 25?
        app.level = 1
        exitBlockProportion = 0.6
        app.exitBlock = exitBlock(app.maze.maze, exitBlockProportion, app)
        app.maze.addExit(app.exitBlock)
        app.player = Player(app, app.maze)
        app.enemy = Enemy(app, app.maze)
        app.playerShadow = PlayerShadow(app)

        # https://obsydianx.itch.io/horror-sfx-volume-1
        app.backgroundSound = dynamicSound('./assets/footsteps.mp3', 1000) 
        # https://www.youtube.com/watch?v=zzXw1E1dX-w
        app.mommySound = dynamicSound('./assets/mommy.mp3', 400)
        # https://www.youtube.com/watch?v=F2hvl2iOI8k
        app.collisionSound = Sound('./assets/collision.mp3')
        # https://freetts.com/
        app.introSound = Sound('./assets/introVoice.mp3')
        app.introSound.start(0)
        # https://freetts.com/
        app.legalInformationSound = Sound('./assets/introVoice2.mp3')
        app.doorSound = Sound('./assets/introVoice3.mp3')

        #Init sprites
        app.sprites = self.initSprites(app)
        # app.sprites = [Sprite(self.otherSprites[3], 16, 1, 3, app) ]

        app.raycaster = Raycaster(app, app.maze)

        # Player can be in same cell for up to 0.25 seconds before dying
        secondsToDie = 0.25
        mstoDie = secondsToDie*1000
        app.dieIntervals = mstoDie//app.timerDelay
        app.collisionCounter = 0
        app.collisionImage = app.loadImage('./assets/bonziLooking.png')
        app.death = Death(app)

        app.win = Win(app)
        app.exitOpen = False

        # Counting something but not seconds? 
        # Seems to be counting like 2/3rds of a second
        app.lastTime = time.time()
            
        app.secondCounter = 1
        app.intervalsPerSecond = 1000//app.timerDelay
        app.currentSecondInterval = 1

# Game Logic
    def gameFlow(self, app):
        if time.time() > app.lastTime + 1:
            app.secondCounter += 1
            app.lastTime = time.time()

        if self.playingDoorSound == False and app.secondCounter == 25:
            app.doorSound.start(0)
            self.playingDoorSound = True
        if self.playingLegalSound == False and app.secondCounter == 40:
            app.legalInformationSound.start(0)
            self.playingLegalSound = True

    def timerFired(self, app):
        # print(app.player.angle)
        self.gameFlow(app) 
        adjustBackgroundVolume(app)

        if app.secondCounter >= 120 and app.exitOpen != True:
            app.exitOpen = True
            app.sprites.append(app.exitBlock.spriteRepresentation)
        if app.secondCounter > 120:
             checkCollision(app)
        if app.secondCounter > 25:
            app.enemy.timerFired(app)
        app.playerShadow.timerFired(app)

    def keyPressed(self, app, event):
        app.player.keyPressed(app, event)
        # https://piazza.com/class/l754ykydwsd6yq/post/3469
        # ^ Explanation for why calling timerFired in keyPressed
        app.game.timerFired(app)
        if event.key == 'g':
            app.displayMap = not app.displayMap

    def drawStartText(self, app, canvas):
        if app.secondCounter in range(4,8):
            canvas.create_text(app.width//2, app.height-100, 
            text='To move your drone press or hold the WASD keys', 
            fill=rgbString(255,204,0), font='Helvetica 26 bold')
        if app.secondCounter in range(8, 12):
            canvas.create_text(app.width//2, app.height-100, 
            text="To change the drone's camera angle press of hold the keys K and L", 
            fill=rgbString(255,204,0), font='Helvetica 26 bold')

    def redraw(self, app, canvas):
        
        app.raycaster.redraw(app, canvas)
        self.drawStartText(app, canvas)

        # Commented out 2d representation debugging code
        if app.displayMap:
            app.maze.redraw(app, canvas)
            app.exitBlock.redraw(app, canvas)
            app.player.redraw(app, canvas)
            app.enemy.redraw(app, canvas)

            canvas.create_text(app.width//2, app.height//2, text=f"{app.secondCounter}",
            fill='white')

            canvas.create_text(app.width//2, -100 + app.height//2, text=f"{app.player.angle}",
            fill='green')

            canvas.create_text(app.width - 100, 100, text='g to toggle minimap',
            fill='white')

    def appStopped(self, app):
        app.backgroundSound.appStopped(app)
        app.mommySound.appStopped(app)