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
import time

class Enemy:
    def __init__(self, app, maze):
        self.maze = maze
        self.xPos, self.yPos, self.row, self.col = self.spawn(app, 15, 35)
        self.lastX = self.xPos - 500
        self.lastY = self.yPos - 500
        self.lastRow = 1
        self.lastCol = 1
        self.xVel = 0
        self.yVel = 0
        self.state = 'wandering'
        self.visited = set()
        self.movingBack = []
        # Adjust speeds. 
        self.wanderSpeed = (app.player.moveVel)*3
        self.huntSpeed = (app.player.moveVel)*1.5
        self.followSpeed = (app.player.moveVel)*0.75
        self.runAwaySpeed = (app.player.moveVel)*3
        self.peekAndStareFar = (app.player.moveVel)*2
        # enemySize probably not needed after sprite animated
        self.enemySize = app.player.playerSize
        self.collisionDist = 15

        # For peek and stare
        self.rowTo = 5
        self.goTo = 5

        # Timer logic for follow
        # only change secondsToWait
        secondsToFollow = 30
        msToFollow = secondsToFollow*1000
        self.followIntervals = msToFollow//app.timerDelay
        self.currentInterval = 0

        self.stareIntervals = 15
        self.currentStareInterval = 0

        # Implementation inspired by my previous work for Hack112
        # https://github.com/KyleleeSea/slashnbash/blob/main/earth_enemy.py
        # https://danaida.itch.io/animated-monsters-pack
        # Load spritesheets
        self.animationCounter = 0
        self.allAnim = []

        for i in range(1,6):
            path = f'./assets/enemy{i}.png'
            animation = app.loadImage(path)
            self.allAnim.append(animation)

        self.spriteVisual = Sprite(self.allAnim[0], 64, self.row, self.col,
        app)

        self.stuckCounter = 0
        self.timeWandering = 0
        self.lastWanderTime = time.time()

# Controller 
    def spawn(self, app, lowerBound, upperBound):
        while True:
            row = random.randint(1, self.maze.size - 1)
            col = random.randint(1, self.maze.size - 1)
            # Check 1) Cell open. 2) Cell reasonably far from player
            distFromPlayer = getDistance(row, col, app.player.row, 
            app.player.col)
            if (distFromPlayer > lowerBound and distFromPlayer < upperBound
            and app.maze.maze[row][col] == 0):
                bounds = getCellBounds(row, col, self.maze.maze, app)
                # Average of bounds to get midpoint
                xPos = (bounds[0] + bounds[2])//2
                yPos = (bounds[1] + bounds[3])//2
                return (xPos, yPos, row, col)

# Controller move functions
# Actions
    def stare(self, app):
        if app.secondCounter > 120:
            self.state = 'wandering'

        if self.state == 'stareNotFound':
            if self.checkPlayerNearby(app):
                self.state = 'stare'
            
            self.follow(app)
        
        if self.state == 'stare':
            self.changeVelRunAway(0, 0)
        
        if self.state == 'stareAway':
            # <2 rather than == to avoid bugs regarding edge of cells
            distFromGoal = getDistance(self.row, self.col, self.rowTo, 
            self.colTo)
            if distFromGoal < 2:
                self.state = 'stareNotFound'
            
            self.runAway(app)

    def peek(self, app):
        if app.secondCounter > 60:
            self.state = 'stareNotFound'

        if self.state == 'peekToPlayer':
            if self.checkPlayerNearby(app):
                self.state = 'peekAway'
                goTo = self.spawn(app, 8, 15)
                self.rowTo = goTo[2]
                self.colTo = goTo[3]
            self.follow(app)
        
        if self.state == 'peekAway':
            # <2 rather than == to avoid bugs regarding edge of cells
            if getDistance(self.row, self.col, self.rowTo, self.colTo) < 2:
                self.state = 'peekToPlayer'

            self.runAway(app)
            
    def wander(self, app):
        if self.check2LenStraightLine(app):
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
                print('moving back')
                print(self.movingBack)
                self.movingBack.pop()
                # Move back to last cell 
                lastCell = self.movingBack[-1]
                moveY = lastCell[0] - self.row
                moveX = lastCell[1] - self.col
                self.changeVelWander(moveX, moveY)
                # Remove so player keeps backtracking
            # Worst case scenario, go random cell
            else:
                print('random')
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
        # Also check and state==following because function used in peek & stare
        if (self.currentInterval >= self.followIntervals
         and self.state=='following'):
            self.currentInterval = 0
            self.state = 'wandering'
        
        if (self.row, self.col) != (app.player.row, app.player.col):
            moveTowardRow, moveTowardCol = shortestPath((self.row, self.col), 
            app, (app.player.row, app.player.col))[-1]
            moveRow, moveCol = (moveTowardRow-self.row, moveTowardCol-self.col)

            if ((self.state == 'stareNotFound' or self.state == 'peekToPlayer')
            and getDistance(self.row, self.col, app.player.row, app.player.col)
            > 6):
                self.changeVelPeekAndStareFar(moveCol, moveRow)
            else:
                self.changeVelFollow(moveCol, moveRow)

# Action Helpers
    def runAway(self, app):
        path = shortestPath((self.row, self.col), 
        app, (self.rowTo, self.colTo))

        if len(path) > 0:
            moveTowardRow, moveTowardCol = path[-1]
            moveRow, moveCol = (moveTowardRow-self.row, 
            moveTowardCol-self.col)
            self.changeVelRunAway(moveCol, moveRow)

    def checkPlayerNearby(self, app):
        if self.checkFullStraightLine(app):
            return True

        dist = getDistance(self.row, self.col, app.player.row, app.player.col)
        if dist < 3:
            return True

        return False

    def checkFullStraightLine(self, app):
        dirs = [(0,1), (0, -1), (1,0), (-1, 0), (-1,1), (-1,-1),(1,1),(1,-1)]
        for direction in dirs:
            newRow = self.row + direction[0]
            newCol = self.col + direction[1]
            if (newRow < 0 and newRow >= len(app.maze.maze) and 
            newCol < 0 and newCol >= len(app.maze.maze)):
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
            cell2[0] >= 0 and cell2[0] < len(self.maze.maze) and
            cell1[1] >= 0 and cell1[1] < len(self.maze.maze) and
            cell2[1] >= 0 and cell2[1] < len(self.maze.maze)):
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

    def changeVelRunAway(self, xChange, yChange):
        self.xVel = self.runAwaySpeed*xChange
        self.yVel = self.runAwaySpeed*yChange

    def changeVelPeekAndStareFar(self, xChange, yChange):
        self.xVel = self.peekAndStareFar*xChange
        self.yVel = self.peekAndStareFar*yChange

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

# Action logic
    def animationUpdates(self, app):
        self.animationCounter += 1
        if self.animationCounter >= len(self.allAnim):
            self.animationCounter = 0
        self.spriteVisual.image = self.allAnim[self.animationCounter]


    def ensureNotStuck(self, app):
        if (self.xPos == self.lastX and 
        self.yPos == self.lastY):
            self.stuckCounter += 1
        
        if self.stuckCounter > 50:
            self.state = 'wandering'
            self.stuckCounter = 0
            self.wander(app)

    def movementUpdates(self, app):
        # Freeze as soon as enter row and col of player
        # Unless going to peek or stare away cell
        if ((self.row, self.col) != (app.player.row, app.player.col) or
        self.state=='peekAway' or self.state=='stareAway'):
            (cellWidth, cellHeight) = getCellSpecs(app, self.maze.maze)
            (xDiffPos, xDiffNeg, yDiffPos, yDiffNeg) = (self.lastX+cellWidth-5,
            self.lastX-cellWidth+5, self.lastY+cellHeight-5, 
            self.lastY-cellHeight+5)

            if (self.xPos > xDiffPos or self.xPos < xDiffNeg or 
            self.yPos > yDiffPos or self.yPos < yDiffNeg):
                self.lastX = self.xPos
                self.lastY = self.yPos
                self.changeState(app)
            
            self.move()
            self.updateRowCol(app)

        if self.state == 'following':
            self.currentInterval += 1
        
        if self.state == 'stare':
            self.currentStareInterval += 1
            if self.currentStareInterval >= self.stareIntervals:
                self.state = 'stareAway'
                self.currentStareInterval = 0
                goTo = self.spawn(app, 8, 15)
                self.rowTo = goTo[2]
                self.colTo = goTo[3]
                self.runAway(app)

        if self.state == 'wandering' and self.timeWandering > 45:
            self.state = 'following'
            self.timeWandering = 0
        
        if time.time() > self.lastWanderTime+1:
            self.lastWanderTime = time.time()
            self.timeWandering += 1

    def timerFired(self, app):
        self.ensureNotStuck(app)
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
        elif self.state == 'peekToPlayer' or self.state == 'peekAway':
            self.peek(app)
        elif (self.state == 'stare' or self.state == 'stareNotFound' or
        self.state == 'stareAway'):
            self.stare(app)

# View 2D (visual representation for 3D)
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - 
        self.enemySize, self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0//7, y0//7, x1//7, y1//7, fill='orange')

