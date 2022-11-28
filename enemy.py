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
from spriteCaster import *

class Enemy:
    def __init__(self, app, maze):
        self.maze = maze
        self.xPos, self.yPos, self.row, self.col = self.spawn(app)
        # May have to change lastRow and lastCol if we end up starting the
        # player in a random location. Current logic: Player starts at 1,1
        # so there's no way the enemy has already visited 1,1 at the start 
        self.lastRow = 1
        self.lastCol = 1
        self.lastX = self.xPos-500
        self.lastY = self.yPos-500
        self.xVel = 0
        self.yVel = 0
        self.state = 'wandering'
        self.visited = set()
        self.movingBack = []
        # Adjust speeds. 
        self.wanderSpeed = (app.player.moveVel)*1.2
        self.huntSpeed = (app.player.moveVel)*2
        self.followSpeed = (app.player.moveVel)*0.95
        # enemySize probably not needed after sprite animated
        self.enemySize = int(min(app.width, app.height)//(len(self.maze.maze)*4))

        # Timer logic for follow
        # only change secondsToWait
        secondsToFollow = 30
        msToFollow = secondsToFollow*1000
        self.followIntervals = msToFollow//app.timerDelay
        self.currentInterval = 0

        # Implementation inspired by my previous work for Hack112
        # https://github.com/KyleleeSea/slashnbash/blob/main/earth_enemy.py
        # Load spritesheets
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
# Controller 
    def spawn(self, app):
        while True:
            row = random.randint(1, self.maze.size - 1)
            col = random.randint(1, self.maze.size - 1)
            # Check 1) Cell open. 2) Cell reasonably far from player
            if (self.maze.maze[row][col] == 0 and 
                (row+col) >= self.maze.size//1.5):
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
        directions = [(0,1), (0, -1), (1,0), (-1, 0)]
        for direction in directions:
            newRow = self.row + direction[0]
            newCol = self.col + direction[1]
            if self.isInBounds(newRow, newCol):
                dist = getDistance(app.player.row, app.player.col, newRow, newCol)
                if dist < bestDist:
                    bestDist = dist
                    bestDir = direction
        self.changeVelFollow(bestDir[1], bestDir[0])

# Action Helpers
    def checkStraightLine(self, app):
        # Note: Currently not checking diagonals
        directions = [(0,1), (0, -1), (1,0), (-1, 0)]
        for direction in directions:
            yAdj, xAdj = direction
            cell1 = (self.row + yAdj, self.col + xAdj)
            cell2 = (self.row + yAdj*2, self.col + xAdj*2)
            # Check cells are open
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
    def animationUpdates(self, app):
        if self.state == 'wandering':
            self.animationCounter += 1 

            if self.animationCounter >= len(self.wanderAnim):
                self.animationCounter = 0
        elif self.state == 'hunting' or self.state == 'startHunting':
            self.animationCounter += 1 

            if self.animationCounter >= len(self.huntAnim):
                self.animationCounter = 0
        elif self.state == 'following':
            self.animationCounter += 1 

            if self.animationCounter >= len(self.followAnim):
                self.animationCounter = 0

    def movementUpdates(self, app):
        # Only update state if in new row or new col
        (cellWidth, cellHeight) = getCellSpecs(app, self.maze.maze)
        (xDiffPos, xDiffNeg, yDiffPos, yDiffNeg) = (self.lastX+cellWidth-5,
        self.lastX-cellWidth+5, self.lastY+cellHeight-5, self.lastY-cellHeight+5)

        if (self.xPos > xDiffPos or self.xPos < xDiffNeg or 
        self.yPos > yDiffPos or self.yPos < yDiffNeg):
            # print(self.state)
        # if self.row != self.lastRow or self.col != self.lastCol:
            self.changeState(app)
            self.lastX = self.xPos
            self.lastY = self.yPos
        # Always move
        self.move()
        # self.lastRow = self.row
        # self.lastCol = self.col
        self.updateRowCol(app)

        if self.state == 'following':
            # print(self.currentInterval, self.followIntervals)
            self.currentInterval += 1        
        
    def timerFired(self, app):
        self.movementUpdates(app)
        self.animationUpdates(app)


    def changeState(self, app):
        if self.state == 'wandering':
            self.wander(app)
        elif self.state == 'startHunting':
            self.startHunt(app)
        elif self.state == 'hunting':
            self.hunt(app)
        elif self.state == 'following':
            self.follow(app)

# View
    def redraw(self, app, canvas):
        if self.state == 'wandering':
            animation = self.wanderAnim[self.animationCounter]
        elif self.state == 'hunting' or self.state == 'startHunting':
            animation = self.huntAnim[self.animationCounter]
        elif self.state == 'following':
            animation = self.followAnim[self.animationCounter]

        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - self.enemySize,
        self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0//4, y0//4, x1//4, y1//4, fill='purple')
        
        # first two args change position center
        # might have to rescale here...
        if app.enemyIsVisible:
            (x, y) = getSpriteCoords(app)
            baseWidthInPx = 48.19
            enemy3DSize = getSpriteDims(app)/baseWidthInPx
            if enemy3DSize > 30:
                enemy3DSize = 30
            if enemy3DSize > 0.5:
                image = app.scaleImage(animation, enemy3DSize)
                canvas.create_image(x, 
                y, image=ImageTk.PhotoImage(image))