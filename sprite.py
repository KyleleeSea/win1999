# https://wynnliam.github.io/raycaster/news/tutorial/2019/04/03/
# raycaster-part-02.html
# https://lodev.org/cgtutor/raycasting3.html
# https://www.youtube.com/watch?v=kyI-Ken7aAk

from cmu_112_graphics import *
from helpers import *
import math

class Sprite:
    def __init__(self, path, baseSize, row, col, app):
        self.path = path
        if type(path) == str:
            self.image = app.loadImage(path)
        # for case enemy
        else:
            self.image = path

        self.baseSize = baseSize

        bounds = getCellBounds(row, col, app.maze.maze, app)

        self.row = row
        self.col = col
        self.xPos = (bounds[0] + bounds[2])//2
        self.yPos = (bounds[1] + bounds[3])//2

# returnX error moves left when player looks left, when should be
# moving right
    def getSpriteCoords(self, app):
        fov = 60
        hX = self.xPos - app.player.xPos
        hY = self.yPos - app.player.yPos
        p = (math.degrees(math.atan2(-hY, hX)))%360

        q = app.player.angle-90 + (fov/2) - p

        if ((app.player.angle >= 0 and app.player.angle <= 110) and 
        (p >= 270 and p <= 360)):
            q += 360
        if ((app.player.angle >= 270 and app.player.angle <= 360) and
        (p >= 0 and p <= 90)):
            q -= 360
        # print(f'hX {hX} hY {hY} p {p} q {q}')

        # APP.WIDTH - SOLVES DIRECTION ERROR
        returnX = app.width - (q * (app.width / fov))
        returnY = app.height / 2
        # print(returnX)
        return (returnX, returnY)

    def getSpriteDims(self, app):
        dist = getDistance(app.player.xPos, app.player.yPos,
        self.xPos, self.yPos)
        if dist > 0:

            scale = app.distToPlane * (app.wallHeight/dist+0.0000001)
            return scale
        return 1
    
    def inFOV(self, xPos, app):
        if xPos >= 0 and xPos <= app.width:
            return True
        return False
        
    def redraw(self, app, canvas):
        (x, y) = self.getSpriteCoords(app)
        sprite3DSize = self.getSpriteDims(app)/self.baseSize
        # print(sprite3DSize)
        if sprite3DSize < 45 or self.path != './assets/exitSprite.png': 
            # try lower #s later 
            image3D = app.scaleImage(self.image, sprite3DSize)
            canvas.create_image(x, 
            y, image=ImageTk.PhotoImage(image3D))
        elif self.path == './assets/exitSprite.png':
            image3D = app.scaleImage(self.image, sprite3DSize)
            canvas.create_image(x, 
            y, image=ImageTk.PhotoImage(image3D))