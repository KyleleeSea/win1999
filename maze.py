from cmu_112_graphics import *
from helpers import *
import random

class Maze:
    def __init__(self, size):
        self.size = size

    def generateMaze(self, size, proportion):
        maze2D = generate2DList(size)
        protectedCells = getProtectedCells(maze2D)
        # Break starting wall and initialize open cells set
        maze2D[1][1] = 0
        # Creating both a list and a set so we can shuffle through the list
        # But search through the set
        openCellsList = [(1,1)]
        openCellsSet = {(1,1)}

        # moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        while len(openCellsSet) < (size**2)*proportion:
            mazeRecurser(maze2D, protectedCells, openCellsList, openCellsSet)
            for row in maze2D:
                print(row)
            print('-----')
            print(len(openCellsSet))
            print(size**2)
            print((len(openCellsSet) < size**2))
        #     random.shuffle(moves)
        #     random.shuffle(openCellsList)
        #     for openCell in openCellsList:
        #         for move in moves:
        #             (currRow, currCol) = openCell
        #             (adjRow, adjCol) = move
        #             (newRow, newCol) = (currRow+adjRow, currCol+adjCol)
        #             # Check legality
        #             if isLegal(maze2D, newRow, newCol, protectedCells, 
        #             openCellsSet):
        #                 maze2D[newRow][newCol] = 0
        #                 openCellsSet.add((newRow, newCol))
        #                 openCellsList.append((newRow, newCol))
        print(maze2D)



        # return mazeBacktracker(maze2D, protectedCells, openCellsList, 
        # openCellsSet)
        

maze = Maze(10)
maze.generateMaze(10, 0.5)