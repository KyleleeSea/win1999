# Inspiration:
# https://2game.com/us/community/how-does-the-xenomorph-work-in-alien-isolation
# https://www.reddit.com/r/alienisolation/comments/cewiui/question_
# how_does_the_alien_learn/
# https://www.reddit.com/r/gametales/comments/n8euyx/nsfw_what_is_your_
# creepiest_unkillable_enemy_you/
# https://www.reddit.com/r/gamedesign/comments/2gd0xx/enemies_in_a_horror_game/

import random 
from helpers import *

class Enemy:
    def __init__(self, app, maze):
        self.maze = maze
        self.xPos, self.yPos, self.row, self.col = self.spawn(app)
        # May have to change lastRow and lastCol if we end up starting the
        # player in a random location. Current logic: Player starts at 1,1
        # so there's no way the enemy has already visited 1,1 at the start 
        self.lastRow = 1
        self.lastCol = 1
        self.xVel = 0
        self.yVel = 0
        self.state = 'wandering'
        # enemySize probably not needed after sprite animated
        self.enemySize = int(min(app.width, app.height)//(len(self.maze.maze)*4))

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

    def timerFired(self, app):
        # Only update state if in new row or new col
        if self.row != self.lastRow or self.col != self.lastCol:
            self.changeState()
        # Always move
        self.move()
        self.lastRow = self.row
        self.lastCol = self.col
        (self.row, self.col) = getCell(app, self.xPos, self.yPos, self.maze.maze)

    def changeState(self):
        if self.state == 'rushing':
            self.rush()
        elif self.state == 'hunting':
            self.hunt()
        elif self.state == 'wandering':
            self.wander()

    def move(self):
        # Might need to add a legality check here 
        self.xPos += self.xVel
        self.yPos += self.yVel
    
        

# View
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - self.enemySize,
        self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0, y0, x1, y1, fill='purple')
