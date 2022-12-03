# https://www.youtube.com/watch?v=kyI-Ken7aAk

from cmu_112_graphics import *
from helpers import *
import math

class Sprite:
    def __init__(self, path, baseSize, app):
        self.image = app.loadImage(path)
        self.baseSize = baseSize

        bounds = getCellBounds(2, 2, app.maze.maze, app)

        self.xPos = (bounds[0] + bounds[2])//2
        self.yPos = (bounds[1] + bounds[3])//2
    
    def inFOV():
        pass

# returnX error moves left when player looks left, when should be
# moving right
    def getSpriteCoords(self, app):
        fov = 60
        hX = self.xPos - app.player.xPos
        hY = self.yPos - app.player.yPos
        p = ((math.atan2(-hY, hX) * (math.radians(180))))%360

        q = app.player.angle-90 + (fov/2) - p
        if (app.player.angle >= 0 and app.player.angle <= 90 and 
        p >= 270 and p <= 360):
            q += 360
        if (app.player.angle >= 270 and app.player.angle <= 360 and
        p >= 0 and p <= 90):
            q -= 360

        returnX = q * (app.width / fov)
        returnY = app.height / 2
        
        return (returnX, returnY)

    def getSpriteDims(self, app):
        dist = getDistance(app.player.xPos, app.player.yPos,
        self.xPos, self.yPos)

        scale = app.distToPlane * (app.wallHeight/dist)
        return scale
    
    def inFOV(self, xPos, app):
        if xPos >= 0 and xPos <= app.width:
            return True
        return False
    
    def redraw(self, app, canvas):
        (x, y) = self.getSpriteCoords(app)
        sprite3DSize = self.getSpriteDims(app)/self.baseSize
        if sprite3DSize > 15:
            sprite3DSize = 15
        if sprite3DSize > 0.5:
            image3D = app.scaleImage(self.image, sprite3DSize)
            canvas.create_image(x, 
            y, image=ImageTk.PhotoImage(image3D))