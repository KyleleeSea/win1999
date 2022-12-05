from soundClass import *
from helpers import *
# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
class dynamicSound:
    def __init__(self, soundPath, volumeThreshold):
        self.sound = Sound(soundPath)
        self.sound.start(-1)
        self.sound.changeVolume(0.1)
        self.volumeTreshold = volumeThreshold

    def appStopped(self, app):
        self.sound.stop()

    def volumeFormula(self, app, distance):
        if distance > self.volumeTreshold:
            return 0
        volumeAdjuster = distance/(min(app.width, app.height)*1.5)
        if 1.0 - volumeAdjuster <= 0.1:
            return 0.1
        else:
            return 1.0 - volumeAdjuster

# Referencing the variable in main.py. If main.py background volume variable
# changes, will need to adjust this function
def adjustBackgroundVolume(app):
    (enemyX, enemyY, playerX, playerY) = (app.enemy.xPos, 
        app.enemy.yPos, app.player.xPos, app.player.yPos)

    backgroundVolume = app.backgroundSound.volumeFormula(app, 
        getDistance(enemyX, enemyY, playerX, playerY))

    mommySound = app.mommySound.volumeFormula(app, 
        getDistance(enemyX, enemyY, playerX, playerY))

    app.backgroundSound.sound.changeVolume(backgroundVolume)
    app.mommySound.sound.changeVolume(mommySound)