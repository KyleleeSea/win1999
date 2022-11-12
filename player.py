from cmu_112_graphics import *
from helpers import *
import math

class Player:
    def __init__(self, app, maze):
        self.angle = 90
        self.moveVel = int(min(app.width, app.height)//150)
        (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, maze.maze, 
        app)
        self.xPos = int((startX0 + startX1)//2)
        self.yPos = int((startY0 + startY1)//2)
        # playerSize temporary
        self.playerSize = int(min(app.width, app.height)//(len(maze.maze)*2))

    def adjustAngle(self, direction):
        if direction == 'clockwise':
            self.angle = (self.angle + 5) % 360
        
        elif direction == 'counterclockwise' and self.angle >= 5:
            self.angle = (self.angle - 5)
        
        elif direction == 'counterclockwise' and self.angle <= 0:
            self.angle = 360 - 5

    def movePlayer(self):
        # https://www.youtube.com/watch?v=rbokZWrwCJE
        # "Solve a Right Triangle Given an Angle and the Hypotenuse"
        # https://www.tutorialspoint.com/python/number_sin.htm
        self.xPos += self.moveVel * math.sin(self.angle)
        self.yPos += self.moveVel * math.cos(self.angle)

    def keyPressed(self, app, event):
        if event.key == 'd':
            self.adjustAngle('clockwise')
        if event.key == 'a':
            self.adjustAngle('counterclockwise')
        if event.key == 'w':
            self.movePlayer()
    
    def redraw(self, app, canvas):
        canvas.create_oval(self.xPos-self.playerSize, self.yPos-self.playerSize,
        self.yPos + self.playerSize, self.yPos + self.playerSize,
        fill='orange')

    