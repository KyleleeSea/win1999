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
        # May have to change lastRow and lastCol if we end up starting the
        # player in a random location. Current logic: Player starts at 1,1
        # so there's no way the enemy has already visited 1,1 at the start 
        self.xVel = 0
        self.yVel = 0
        # Adjust constantSpeed. Currently 10% faster than player
        self.constantSpeed = int(min(app.width, app.height)//90) 
        # enemySize probably not needed after sprite animated
        self.enemySize = int(min(app.width, app.height)//(len(self.maze.maze)*4))

        # Bug testing variables
        self.goalRow = 1
        self.goalCol = 1
        self.visited = set()

        # Start pathing logic
        self.wander()

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
    def wander(self):
        if self.row == self.goalRow and self.col == self.goalCol:
            self.hunt()
            # Check if return necessary later
            return
        else:
            moves = [(1,0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1),
            (-1, -1)]
            random.shuffle(moves)
            for move in moves:
                newRow = self.row + move[0]
                newCol = self.col + move[1]
                if self.isLegalMove(newRow, newCol):
                    print(f'xVel: {self.xVel}')
                    print(f'yVel: {self.yVel}')
                    print(f'row: {self.row}')
                    print(f'col: {self.col}')
                    self.xVel = self.constantSpeed*move[1]
                    self.yVel = self.constantSpeed*move[0]
                    self.visited.add((newRow, newCol))

                    solution = self.wander()
                    if solution != None:
                        return solution
                    self.xVel = -(self.constantSpeed*move[1])
                    self.yVel = -(self.constantSpeed*move[0])
            return None
        
    def isLegalMove(self, row, col):
        if self.maze.maze[row][col] == 0 and (row, col) not in self.visited:
            return True
        return False
    
    def hunt(self):
        print('now hunting!')
    

    def timerFired(self, app):
        self.move()
        self.updateRowCol(app)

    def move(self):
        # Might need to add a legality check here 
        self.xPos += self.xVel
        self.yPos += self.yVel

    def updateRowCol(self, app):
        self.row, self.col = getCell(app, self.xPos, self.yPos, self.maze.maze)
    
        

# View
    def redraw(self, app, canvas):
        (x0, y0, x1, y1) = (self.xPos - self.enemySize, self.yPos - self.enemySize,
        self.xPos + self.enemySize, self.yPos + self.enemySize)
        canvas.create_oval(x0, y0, x1, y1, fill='purple')
