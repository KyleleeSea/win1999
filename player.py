from cmu_112_graphics import *
from helpers import *
from backgroundLogic import *
from dynamicSound import *
import math

class Player:
    def __init__(self, app, maze):
        # Consider restructuring self.maze and self.exitBlock assignment
        self.lastMousePos = None
        self.mouseSensitivityDenominator = int(min(app.width, app.height)//550)
        self.maze = maze.maze
        self.exitBlock = maze.exitBlock
        self.angle = 90
        self.angleVel = 10 #Test
        self.moveVel = app.cellWidth//15
        #Make player slower by increasing denominator of moveVel 
        (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, self.maze, 
        app)
        self.xPos = ((startX0 + startX1)/2)
        self.yPos = ((startY0 + startY1)/2)
        self.row = 1
        self.col = 1
        self.lastRow = 1
        self.lastCol = 1
        # playerSize for 2d debugging representation
        self.playerSize = int(app.cellWidth//5)

    def adjustAngle(self, direction):
        if direction == 'clockwise':
            newAngle = (self.angle + self.angleVel)
            if newAngle > 360:
                self.angle = newAngle - 360
            else:
                self.angle = newAngle
        
        elif direction == 'counterclockwise' and self.angle > self.angleVel:
            self.angle = (self.angle - self.angleVel)
        
        elif direction == 'counterclockwise' and self.angle == self.angleVel:
            self.angle = 360
        
        elif direction == 'counterclockwise' and self.angle < self.angleVel:
            self.angle = 360 - self.angleVel

    def movePlayer(self, app, direction):
        # https://www.youtube.com/watch?v=rbokZWrwCJE
        # "Solve a Right Triangle Given an Angle and the Hypotenuse"
        # https://www.tutorialspoint.com/python/number_sin.htm
        # https://www.geeksforgeeks.org/degrees-and-radians-in-python/
        # Must convert to radians. Sin and cos in radians

        newX = self.xPos + self.moveVel * math.sin(math.radians(self.angle
        -90*direction))
        newY = self.yPos + self.moveVel * math.cos(math.radians(self.angle
        -90*direction))
        if checkLegalMove(self.lastCol, self.lastRow, newX, newY, self.maze, app):
            self.xPos = newX
            self.yPos = newY
            self.row, self.col = getCell(app, newX, newY, self.maze)
            # Commented out next level functionality for MVP
            if app.exitOpen and self.checkExit(self.exitBlock):
                app.mode = 'win'
        # Row col updating for shadow logic
        if self.row != self.lastRow or self.col != self.lastCol:
            # Account for starter value
            if self.lastRow != 0 and self.lastCol != 0:
                app.playerShadow.addToVisited((self.lastRow, self.lastCol))
        self.lastRow = self.row
        self.lastCol = self.col
        self.updateRowCol(app)

    def updateRowCol(self, app):
        self.row, self.col = getCell(app, self.xPos, self.yPos, self.maze)

    def keyPressed(self, app, event):
        if event.key == 'w':
            self.movePlayer(app, 0)
        if event.key == 'd':
            self.movePlayer(app, -1)
        if event.key == 'a':
            self.movePlayer(app, 1)
        if event.key == 's':
            self.movePlayer(app, 2)
        elif event.key == 'l':
            self.adjustAngle('clockwise')
        elif event.key == 'k':
            self.adjustAngle('counterclockwise')

    def mouseMoved(self, app, event):
        if self.lastMousePos == None:
            self.lastMousePos = event.x
        else:
            diff = event.x - self.lastMousePos
            self.lastMousePos = event.x
            self.adjustAngle(diff//self.mouseSensitivityDenominator)

    def checkExit(self, exitBlock):
        if (self.row, self.col) == (exitBlock.row, exitBlock.col):
            return True
        return False

    def redraw(self, app, canvas):
        canvas.create_oval((self.xPos-self.playerSize)//7, 
        (self.yPos-self.playerSize)//7,
        (self.xPos + self.playerSize)//7, (self.yPos + self.playerSize)//7,
        fill='orange')
        # Temporary 2D debugging line that'll show angle facing
        canvas.create_line(self.xPos//7, self.yPos//7, 
        (self.xPos+(self.moveVel * math.sin(math.radians(self.angle)))*10)//7,
        (self.yPos+self.moveVel * math.cos(math.radians(self.angle))*10)//7, 
        fill='red')
