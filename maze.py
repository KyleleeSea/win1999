from cmu_112_graphics import *
from helpers import *

class Maze:
    def __init__(self, size):
        self.size = size

    def generateMaze(self, size):
        maze = generate2DList(size)
        protectedCells = getProtectedCells(maze)
        # Break starting wall and initialize open cells set
        maze[1][1] = 0
        # Creating both a list and a set so we can shuffle through the list
        # But search through the set
        openCellsList = [(1,1)]
        proportion = 0.5
        
        while not mazeIsFinished(maze, openCellsList, proportion):
            changeMazeTile(maze, protectedCells, openCellsList)
            for row in maze:
                print(row)
            print('-----')
        return maze

maze = Maze(10)
maze.generateMaze(20)