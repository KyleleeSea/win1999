from soundClass import *
from helpers import *

class backgroundSound:
    def __init__(self, soundPath):
        self.sound = Sound(soundPath)
        self.sound.start(-1)
        self.sound.changeVolume(0.1)

    def appStopped(self, app):
        self.sound.stop()

    def volumeFormula(self, app, distance):
        volumeAdjuster = distance/(min(app.width, app.height)*1.5)
        if 1.0 - volumeAdjuster <= 0.1:
            return 0.1
        else:
            return 1.0 - volumeAdjuster

# Referencing the variable in main.py. If main.py background volume variable
# changes, will need to adjust this function
def adjustBackgroundVolume(app):
    (exitX, exitY, playerX, playerY) = (app.exitBlock.xPos, 
        app.exitBlock.yPos, app.player.xPos, app.player.yPos)

    backgroundVolume = app.backgroundSound.volumeFormula(app, 
        getDistance(exitX, exitY, playerX, playerY))

    app.backgroundSound.sound.changeVolume(backgroundVolume)