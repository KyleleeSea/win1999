from cmu_112_graphics import *
from helpers import *

class Maze:
    def __init__(self, size):
        self.size = size

    def generateMaze(self, size):
        maze2D = generate2DList(size)
        protectedCells = getProtectedCells(maze2D)
        # Break starting wall and initialize open cells set
        maze2D[1][1] = 0
        # Creating both a list and a set so we can shuffle through the list
        # But search through the set
        openCellsList = [(1,1)]
        openCellsSet = {(1,1)}

        return mazeBacktracker(maze2D, protectedCells, openCellsList, 
        openCellsSet)
        

maze = Maze(10)
maze.generateMaze(10)