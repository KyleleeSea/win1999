from cmu_112_graphics import *
from helpers import *
from backgroundLogic import *
from backgroundSound import *
import math

class Player:
    def __init__(self, app, maze):
        # Consider restructuring self.maze and self.exitBlock assignment
        self.lastMousePos = None
        self.mouseSensitivityDenominator = int(min(app.width, app.height)//400)
        self.maze = maze.maze
        self.exitBlock = maze.exitBlock
        self.angle = 90
        # self.angleVel = 10
        self.moveVel = int(min(app.width, app.height)//100) 
        #Make player slower by increasing denominator of moveVel for actual
        # game. Maybe 150?
        (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, self.maze, 
        app)
        self.xPos = int((startX0 + startX1)//2)
        self.yPos = int((startY0 + startY1)//2)
        self.row = 1
        self.col = 1
        # playerSize temporary
        self.playerSize = int(min(app.width, app.height)//(len(maze.maze)*4))

    def adjustAngle(self, angleDiff):
        self.angle = (self.angle - angleDiff) % 360

    def movePlayer(self, app):
        # https://www.youtube.com/watch?v=rbokZWrwCJE
        # "Solve a Right Triangle Given an Angle and the Hypotenuse"
        # https://www.tutorialspoint.com/python/number_sin.htm
        # https://www.geeksforgeeks.org/degrees-and-radians-in-python/
        # Must convert to radians. Sin and cos in radians

        newX = self.xPos + self.moveVel * math.sin(math.radians(self.angle))
        newY = self.yPos + self.moveVel * math.cos(math.radians(self.angle))
        if checkLegalMove(newX, newY, self.maze, app):
            self.xPos = newX
            self.yPos = newY
            self.row, self.col = getCell(app, newX, newY, self.maze)
            adjustBackgroundVolume(app)
            if self.checkExit(self.exitBlock):
                #nextLevel from backgroundLogic.py
                nextLevel(app)

    def keyPressed(self, app, event):
        if event.key == 'w':
            self.movePlayer(app)

    def mouseMoved(self, app, event):
        if self.lastMousePos == None:
            self.lastMousePos = event.x
        else:
            diff = event.x - self.lastMousePos
            self.lastMousePos = event.x
            self.adjustAngle(diff//self.mouseSensitivityDenominator)

    def checkExit(self, exitBlock):
        if exitBlock.row == self.row and exitBlock.col == self.col:
            return True
        return False

    def redraw(self, app, canvas):
        canvas.create_oval(self.xPos-self.playerSize, self.yPos-self.playerSize,
        self.xPos + self.playerSize, self.yPos + self.playerSize,
        fill='orange')

        # Temporary 2D debugging line that'll show angle facing
        canvas.create_line(self.xPos, self.yPos, 
        self.xPos+(self.moveVel * math.sin(math.radians(self.angle)))*10,
        self.yPos+self.moveVel * math.cos(math.radians(self.angle))*10, 
        fill='orange')