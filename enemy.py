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
from shortestPath import *
from sprite import *

class Enemy:
    def __init__(self, app, maze):
        self.maze = maze
        self.xPos, self.yPos, self.row, self.col = self.spawn(app)
        self.lastX = self.xPos - 500
        self.lastY = self.yPos - 500
        self.lastRow = 1
        self.lastCol = 1
        self.xVel = 0
        self.yVel = 0
        self.state = 'following'
        self.visited = set()
        self.movingBack = []
        # Adjust speeds. 
        self.wanderSpeed = (app.player.moveVel)*1.5
        self.huntSpeed = (app.player.moveVel)*1.5
        self.followSpeed = (app.player.moveVel)*0.75
        # enemySize probably not needed after sprite animated
        self.enemySize = app.player.playerSize
        self.collisionDist = 15

        # Timer logic for follow
        # only change secondsToWait
        secondsToFollow = 30
        msToFollow = secondsToFollow*1000
        self.followIntervals = msToFollow//app.timerDelay
        self.currentInterval = 0

        # Implementation inspired by my previous work for Hack112
        # https://github.com/KyleleeSea/slashnbash/blob/main/earth_enemy.py
        # Load spritesheets
        # https://www.deviantart.com/thenoahguy1/art/Bonzi-spritesheet-440805977
        spritesheet = app.loadImage('./assets/bonziBuddy.png')
        startX = 0
        xWidth = 60.23
        self.animationCounter = 0


        self.wanderAnim = []
        (startY, endY) = getYs(5)
        for i in range(7):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.wanderAnim.append(animation)
        for i in range(10,14):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.wanderAnim.append(animation)

        self.huntAnim = []
        (startY, endY) = getYs(14)
        for i in range(8,17):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.huntAnim.append(animation)
        (startY, endY) = getYs(15)
        for i in range(8):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.huntAnim.append(animation)

        self.followAnim = []
        (startY, endY) = getYs(9)
        for i in range(2,11):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.followAnim.append(animation)
        for i in range(11,3,-1):
            animation = cutSpritesheet(startX, xWidth*i, xWidth, startY, 
            endY, spritesheet, app)
            self.followAnim.append(animation)

        self.spriteVisual = Sprite(self.wanderAnim[0], 48, self.row, self.col,
        app)

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
        if self.checkFullStraightLine(app):
            self.visited = set()
            self.movingBack = []
            self.state = 'following'

        huntTuple = self.huntingRangeCheck(app)
        if huntTuple != None:
            self.changeVelHunt(huntTuple[1], huntTuple[0])
            self.state = 'startHunting'
        else:
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
        if self.check2LenStraightLine(app):
            self.state = 'following'
        # Check shadow exists 
        if len(app.playerShadow.shadow) == 0:
            self.state = 'wandering'
            return
        else:
            # Find place of current cell in shadow
            if (self.row, self.col) not in app.playerShadow.shadow:
                # Reseting shadow here may cause bugs. Come back.
                app.playerShadow.shadow = []
                self.state = 'wandering'
                return

            currShadowIndex = app.playerShadow.shadow.index((self.row, self.col))

            if len(app.playerShadow.shadow) <= currShadowIndex+1:
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

# https://brilliant.org/wiki/a-star-search/
# https://isaaccomputerscience.org/concepts/dsa_search_a_star
# https://www.youtube.com/watch?v=-L-WgKMFuhE
    def follow(self, app):
        if self.currentInterval >= self.followIntervals:
            self.currentInterval = 0
            self.state = 'wandering'
        
        if (self.row, self.col) != (app.player.row, app.player.col):
            moveTowardRow, moveTowardCol = shortestPath((self.row, self.col), 
            app, (app.player.row, app.player.col))[-1]
            moveRow, moveCol = (moveTowardRow-self.row, moveTowardCol-self.col)
            self.changeVelFollow(moveCol, moveRow)

# Action Helpers
    def checkFullStraightLine(self, app):
        dirs = [(0,1), (0, -1), (1,0), (-1, 0)]
        for direction in dirs:
            newRow = self.row + direction[0]
            newCol = self.col + direction[1]
            while app.maze.maze[newRow][newCol] != 1:
                if (app.player.row, app.player.col) == (newRow, newCol):
                    return True
                newRow += direction[0]
                newCol += direction[1]
        return False

    def check2LenStraightLine(self, app):
        # Note: Currently not checking diagonals
        directions = [(0,1), (0, -1), (1,0), (-1, 0), (1,1), (1,-1), (-1,1),
        (-1,-1)]
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
            if ((self.row + move[0], self.col + move[1]) in 
            app.playerShadow.shadow):
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
        if (row >= 0 and row < len(self.maze.maze) and col >= 0 and 
        col < len(self.maze.maze)):
            if self.maze.maze[row][col] == 0:
                return True
        return False
    
    def notVisitedAndInBounds(self, row, col):
        if self.isInBounds(row, col) and (row, col) not in self.visited:
            return True
        return False

    def move(self):
        self.xPos += self.xVel
        self.yPos += self.yVel
        self.spriteVisual.xPos += self.xVel
        self.spriteVisual.yPos += self.yVel

    def updateRowCol(self, app):
        self.row, self.col = getCell(app, self.xPos, self.yPos, self.maze.maze)
        self.spriteVisual.row = self.row
        self.spriteVisual.col = self.col
    
    def rushCondition(self):
        pass

# Action logic
    def animationUpdates(self, app):
        if self.state == 'wandering':
            self.animationCounter += 1
            if self.animationCounter >= len(self.wanderAnim):
                self.animationCounter = 0
            self.spriteVisual.image = self.wanderAnim[self.animationCounter]
        elif self.state == 'hunting' or self.state == 'startHunting':
            self.animationCounter += 1 

            if self.animationCounter >= len(self.huntAnim):
                self.animationCounter = 0
            self.spriteVisual.image = self.huntAnim[self.animationCounter]
        elif self.state == 'following':
            self.animationCounter += 1 

            if self.animationCounter >= len(self.followAnim):
                self.animationCounter = 0
            self.spriteVisual.image = self.followAnim[self.animationCounter]

    def movementUpdates(self, app):
        # Only update state if in new row or new col
        # if self.row != self.lastRow or self.col != self.lastCol:
        #     self.changeState(app)
        # # Always move
        # self.move()
        # self.lastRow = self.row
        # self.lastCol = self.col
        # Freeze as soon as enter row and col of player
        if (self.row, self.col) != (app.player.row, app.player.col):
            (cellWidth, cellHeight) = getCellSpecs(app, self.maze.maze)
            (xDiffPos, xDiffNeg, yDiffPos, yDiffNeg) = (self.lastX+cellWidth-5,
            self.lastX-cellWidth+5, self.lastY+cellHeight-5, 
            self.lastY-cellHeight+5)

            if (self.xPos > xDiffPos or self.xPos < xDiffNeg or 
            self.yPos > yDiffPos or self.yPos < yDiffNeg):
                self.changeState(app)
                self.lastX = self.xPos
                self.lastY = self.yPos
            
            self.move()
            self.updateRowCol(app)

        if self.state == 'following':
            self.currentInterval += 1

    def timerFired(self, app):
        self.animationUpdates(app)
        self.movementUpdates(app)


    def changeState(self, app):
        if self.state == 'wandering':
            self.wander(app)
        elif self.state == 'startHunting':
            self.startHunt(app)
        elif self.state == 'hunting':
            self.hunt(app)
        elif self.state == 'following':
            self.follow(app)

# View 2D (visual representation for 3D)
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - 
        self.enemySize, self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0//7, y0//7, x1//7, y1//7, fill='orange')

