# https://www.youtube.com/watch?v=kyI-Ken7aAk

from cmu_112_graphics import *
from helpers import *
import math
from raycaster import *

class Sprite:
    def __init__(self, path, baseSize, row, col, app):
        self.image = app.loadImage(path)
        self.baseSize = baseSize

        bounds = getCellBounds(row, col, app.maze.maze, app)

        self.row = row
        self.col = col
        self.xPos = (bounds[0] + bounds[2])//2
        self.yPos = (bounds[1] + bounds[3])//2

        self.raycasterHelper = Raycaster(app, app.maze)

# returnX error moves left when player looks left, when should be
# moving right
    def getSpriteCoords(self, app):
        fov = 60
        hX = self.xPos - app.player.xPos
        hY = self.yPos - app.player.yPos
        p = (math.degrees(math.atan2(-hY, hX)))%360

        q = app.player.angle-90 + (fov/2) - p
        if (app.player.angle >= 0 and app.player.angle <= 90 and 
        p >= 270 and p <= 360):
            q += 360
        if (app.player.angle >= 270 and app.player.angle <= 360 and
        p >= 0 and p <= 90):
            q -= 360

        # APP.WIDTH - SOLVES DIRECTION ERROR
        returnX = app.width - (q * (app.width / fov))
        returnY = app.height / 2
        
        return (returnX, returnY)

    def getSpriteDims(self, app):
        dist = getDistance(app.player.xPos, app.player.yPos,
        self.xPos, self.yPos)

        scale = app.distToPlane * (app.wallHeight/dist+0.0000001)
        return scale
    
    def inFOV(self, xPos, app):
        if xPos >= 0 and xPos <= app.width:
            return True
        return False
    
    def notBehindWall(self, app):
        if app.player.xPos >= self.xPos:
            xLen = app.player.xPos - self.xPos
        else:
            xLen = self.xPos - app.player.xPos

        if app.player.yPos >= self.yPos:
            yLen = app.player.yPos - self.yPos
        else:
            yLen = self.yPos - app.player.yPos 
        # https://www.w3schools.com/python/ref_math_atan.asp
        anglePlayertoSprite = math.degrees(math.atan(yLen/(xLen+1)))
        ray = self.raycasterHelper.getRay(app, anglePlayertoSprite)
        rayDist = ray['dist']
        dist = getDistance(app.player.xPos, app.player.yPos,
        self.xPos, self.yPos)
        
        if rayDist < dist:
            return False
        else:
            return True
    
    def redraw(self, app, canvas):
        (x, y) = self.getSpriteCoords(app)
        sprite3DSize = self.getSpriteDims(app)/self.baseSize
        if sprite3DSize > 10:
            sprite3DSize = 10
        if sprite3DSize > 0.5:
            image3D = app.scaleImage(self.image, sprite3DSize)
            canvas.create_image(x, 
            y, image=ImageTk.PhotoImage(image3D))