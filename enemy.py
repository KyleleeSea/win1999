# Inspiration:
# https://2game.com/us/community/how-does-the-xenomorph-work-in-alien-isolation
# https://www.reddit.com/r/alienisolation/comments/cewiui/question_
# how_does_the_alien_learn/
# https://www.reddit.com/r/gametales/comments/n8euyx/nsfw_what_is_your_
# creepiest_unkillable_enemy_you/
# https://www.reddit.com/r/gamedesign/comments/2gd0xx/enemies_in_a_horror_game/

import random 
from helpers import *
from backgroundLogic import *

class Enemy:
    def __init__(self, app, maze):
        self.maze = maze
        self.xPos, self.yPos, self.row, self.col = self.spawn(app)
        # Currently subtracting arbitary value to start movement 
        self.lastX = self.xPos-150
        self.lastY = self.yPos-150
        self.xVel = 0
        self.yVel = 0
        self.state = 'wandering'
        self.visited = set()
        self.movingBack = []
        # Adjust speeds. 
        self.wanderSpeed = (app.player.moveVel)*4
        self.huntSpeed = (app.player.moveVel)*2
        self.followSpeed = (app.player.moveVel)*0.95
        # enemySize probably not needed after sprite animated
        self.enemySize = app.player.playerSize
        self.collisionDist = 15

        # Timer logic for follow
        # only change secondsToWait
        secondsToFollow = 30
        msToFollow = secondsToFollow*1000
        self.followIntervals = msToFollow//app.timerDelay
        self.currentInterval = 0

# Controller 
    def spawn(self, app):
        while True:
            row = random.randint(1, self.maze.size - 1)
            col = random.randint(1, self.maze.size - 1)
            # Check 1) Cell open. 2) Cell reasonably far from player
            if (self.maze.maze[row][col] == 0 and 
                (row+col) >= self.maze.size//2 and 
                (row+col) <= self.maze.size//1.5):
                bounds = getCellBounds(row, col, self.maze.maze, app)
                # Average of bounds to get midpoint
                xPos = (bounds[0] + bounds[2])//2
                yPos = (bounds[1] + bounds[3])//2
                return (xPos, yPos, row, col)

# Controller move functions
# Actions
    def wander(self, app):
        if self.checkStraightLine(app):
            # print('found')
            self.visited = set()
            self.movingBack = []
            self.state = 'following'

        huntTuple = self.huntingRangeCheck(app)
        if huntTuple != None:
            # print('smelled player')
            self.changeVelHunt(huntTuple[1], huntTuple[0])
            self.state = 'startHunting'
        else:
            # print('now wandering')

            moves = [(1,0), (-1, 0), (0, 1), (0, -1)]
            # Optimally move to open, non visited cell
            for move in moves:
                newRow = self.row + move[0]
                newCol = self.col + move[1]
                if self.notVisitedAndInBounds(newRow, newCol):
                    self.changeVelWander(move[1], move[0])
                    self.visited.add((newRow, newCol))
                    self.movingBack.append((newRow, newCol))
                    # returning so u don't get to next part
                    return
            # If reached end of path, trying moving back one
            # Remove latest so enemy doesn't stay stationary
            # Check if at least two
            if len(self.movingBack) >= 2:
                # print('moving back')
                # print(self.movingBack)
                self.movingBack.pop()
                # Move back to last cell 
                lastCell = self.movingBack[-1]
                moveY = lastCell[0] - self.row
                moveX = lastCell[1] - self.col
                self.changeVelWander(moveX, moveY)
                # Remove so player keeps backtracking
            # Worst case scenario, go random cell
            else:
                random.shuffle(moves)
                for move in moves:
                    newRow = self.row + move[0]
                    newCol = self.col + move[1]
                    if self.isInBounds(newRow, newCol):
                        self.changeVelWander(move[1], move[0])
                        self.visited.add((newRow, newCol))

    def startHunt(self, app):
        if (self.row, self.col) in app.playerShadow.shadow:
            self.state = 'hunting'
            self.visited = set()
            self.movingBack = []

    def hunt(self, app):
        if self.checkStraightLine(app):
            # print('found')
            self.state = 'following'
        # Check shadow exists 
        if len(app.playerShadow.shadow) == 0:
            self.state = 'wandering'
            return
        else:
            # Find place of current cell in shadow
            # print(f'row, col: {self.row}, {self.col}')
            # print(f'playerShadow: {app.playerShadow.shadow}')
            if (self.row, self.col) not in app.playerShadow.shadow:
                # print('row and col not found')
                # Reseting shadow here may cause bugs. Come back.
                app.playerShadow.shadow = []
                self.state = 'wandering'
                return

            currShadowIndex = app.playerShadow.shadow.index((self.row, self.col))

            if len(app.playerShadow.shadow) <= currShadowIndex+1:
                # print('doesnt have a following cell')
                # Reseting shadow here may cause bugs. Come back.
                app.playerShadow.shadow = []
                self.state = 'wandering'
                return
            # Move to the next cell in player shadow
            moveTo = app.playerShadow.shadow[currShadowIndex+1]
            moveY = moveTo[0] - self.row
            moveX = moveTo[1] - self.col
            app.playerShadow.shadow = app.playerShadow.shadow[currShadowIndex:]
            self.changeVelHunt(moveX, moveY)

    def follow(self, app):
        if self.currentInterval >= self.followIntervals:
            # print('time up')
            self.currentInterval = 0
            self.state = 'wandering'

        bestDir = (0, 0)
        bestDist = 1000
        # Stop movement if already in collision area
        if (getDistance(app.player.yPos, app.player.xPos, self.yPos, self.xPos)
        > self.collisionDist):
            directions = [(0, self.followSpeed), (0, -self.followSpeed),
            (self.followSpeed, 0), (-self.followSpeed, 0)]
            # Utilizes different format from wander and hunt because
            # follow is meant to create collisions, needing more
            # exact movement 
            for direction in directions:
                newX = self.xPos + direction[0]
                newY = self.yPos + direction[1]
                (newRow, newCol) = getCell(app, newX, newY, self.maze.maze)
                if self.isInBounds(newRow, newCol):
                    dist = getDistance(app.player.xPos, app.player.yPos,
                    newX, newY)
                    if dist < bestDist:
                        bestDist = dist
                        bestDir = direction
            self.xPos += bestDir[0]
            self.yPos += bestDir[1]

# Action Helpers
    def checkStraightLine(self, app):
        # Note: Currently not checking diagonals
        directions = [(0,1), (0, -1), (1,0), (-1, 0)]
        for direction in directions:
            yAdj, xAdj = direction
            cell1 = (self.row + yAdj, self.col + xAdj)
            cell2 = (self.row + yAdj*2, self.col + xAdj*2)
            # Check cells are open
            if (cell1[0] >= 0 and cell1[0] < len(self.maze.maze) and
            cell2[0] >= 0 and cell2[0] < len(self.maze.maze)):
                if (self.maze.maze[cell1[0]][cell1[1]] == 0 and 
                self.maze.maze[cell2[0]][cell2[1]] == 0):
                # Check player at open cell 
                    if ((app.player.row, app.player.col) == cell1 or 
                    (app.player.row, app.player.col) == cell2):
                        return True
        return False

    def huntingRangeCheck(self, app):
        moves = [(0,1), (0, -1), (1,0), (-1, 0)]
        for move in moves:
            if (self.row + move[0], self.col + move[1]) in app.playerShadow.shadow:
                return move
        return None

    def changeVelWander(self, xChange, yChange):
        self.xVel = self.wanderSpeed*xChange
        self.yVel = self.wanderSpeed*yChange

    def changeVelHunt(self, xChange, yChange):
        self.xVel = self.huntSpeed*xChange
        self.yVel = self.huntSpeed*yChange

    def changeVelFollow(self, xChange, yChange):
        self.xVel = self.followSpeed*xChange
        self.yVel = self.followSpeed*yChange

    def isInBounds(self, row, col):
        if self.maze.maze[row][col] == 0:
            return True
        return False
    
    def notVisitedAndInBounds(self, row, col):
        if self.isInBounds(row, col) and (row, col) not in self.visited:
            return True
        return False

    def move(self):
        # Might need to add a legality check here 
        self.xPos += self.xVel
        self.yPos += self.yVel

    def updateRowCol(self, app):
        self.row, self.col = getCell(app, self.xPos, self.yPos, self.maze.maze)
    
    def rushCondition(self):
        pass
# Action logic
    def movementUpdates(self, app):
        # Different movement pipeline for following algorithm 
        if self.state == 'following':
            self.follow(app)
            return

        # Only update state if in cell center
        (cellWidth, cellHeight) = getCellSpecs(app, self.maze.maze)
        (xDiffPos, xDiffNeg, yDiffPos, yDiffNeg) = (self.lastX+cellWidth-5,
        self.lastX-cellWidth+5, self.lastY+cellHeight-5, self.lastY-cellHeight+5)

        if (self.xPos > xDiffPos or self.xPos < xDiffNeg or 
        self.yPos > yDiffPos or self.yPos < yDiffNeg):
            self.changeState(app)
            self.lastX = self.xPos
            self.lastY = self.yPos
        # Always move
        self.move()
        self.updateRowCol(app)

        if self.state == 'following':
            # print(self.currentInterval, self.followIntervals)
            self.currentInterval += 1        
        
    def timerFired(self, app):
        self.movementUpdates(app)


    def changeState(self, app):
        if self.state == 'wandering':
            self.wander(app)
        elif self.state == 'startHunting':
            self.startHunt(app)
        elif self.state == 'hunting':
            self.hunt(app)

# View
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - self.enemySize,
        self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0//7, y0//7, x1//7, y1//7, fill='orange')