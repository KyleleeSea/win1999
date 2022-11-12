from cmu_112_graphics import *
from helpers import *
import math

class Player:
    def __init__(self, app, maze):
        self.maze = maze.maze
        self.angle = 90
        self.angleVel = 10
        self.moveVel = int(min(app.width, app.height)//150)
        (startX0, startY0, startX1, startY1) = getCellBounds(1, 1, maze.maze, 
        app)
        self.xPos = int((startX0 + startX1)//2)
        self.yPos = int((startY0 + startY1)//2)
        # playerSize temporary
        self.playerSize = int(min(app.width, app.height)//(len(maze.maze)*4))

    def adjustAngle(self, direction):
        if direction == 'clockwise':
            self.angle = (self.angle + self.angleVel) % 360
        
        elif direction == 'counterclockwise' and self.angle >= 5:
            self.angle = (self.angle - self.angleVel)
        
        elif direction == 'counterclockwise' and self.angle <= 0:
            self.angle = 360 - self.angleVel

    def movePlayer(self, app):
        # https://www.youtube.com/watch?v=rbokZWrwCJE
        # "Solve a Right Triangle Given an Angle and the Hypotenuse"
        # https://www.tutorialspoint.com/python/number_sin.htm
        # https://www.geeksforgeeks.org/degrees-and-radians-in-python/
        # Must convert to radians. Sin and cos in radians

        newX = self.xPos + self.moveVel * math.sin(math.radians(self.angle))
        newY = self.yPos + self.moveVel * math.cos(math.radians(self.angle))
        if self.checkLegalMove(newX, newY, app):
            self.xPos = newX
            self.yPos = newY

    def keyPressed(self, app, event):
        if event.key == 'd':
            self.adjustAngle('clockwise')
        if event.key == 'a':
            self.adjustAngle('counterclockwise')
        if event.key == 'w':
            self.movePlayer(app)

    def checkLegalMove(self, newX, newY, app):
        (row, col) = getCell(app, newX, newY, self.maze)
        if self.maze[row][col] == 0:
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