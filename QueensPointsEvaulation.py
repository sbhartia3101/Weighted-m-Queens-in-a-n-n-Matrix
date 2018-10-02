"""
Created on Sun Sep 16 14:10:42 2018

@author: sweetybhartia
"""

"""
Done using greedy, DFS, A*, and Incompatibility Checks
"""
import numpy as np
import time


class CityMap:
    def __init__(self, gridSize, noOfPolice, noOfScooters, city):
        self.gridSize = gridSize
        self.noOfPolice = noOfPolice
        self.noOfScooters = noOfScooters
        # Original city matrix
        self.city = city

        # Dictionary to specify the column position of a police in a row
        self.rows = {}
        # Dictionary to specify the row position of a police in a column
        self.columns = {}
        # Dictionary to specify the position of a police in a left diagonal (r-c)
        self.leftDiagonals = {}
        # Dictionary to specify the position of a police in a left diagonal (r+c)
        self.rightDiagonals = {}

        # Dictionary to specify the positions of the points in the map
        self.pointsMap = {}
        # Final points
        self.result = 0

        self.points = []
        self.noOfSolutions = 0
        self.inCompatibleGrids ={}

    def createMap(self):
        self.pointsMap = dict(((i, j), self.city[i][j]) for i in range(len(self.city)) for j in range(len(self.city)))
        self.pointsMap = sorted(self.pointsMap.items(), reverse=True, key=lambda (k,v): (v,k))

    # To be used
    def isSafe(self, r, c):
        if (r in self.rows) or (c in self.columns) or ((r - c) in self.leftDiagonals) or (
                (r + c) in self.rightDiagonals):
            return False
        return True

    # Place a police
    def placeAPolice(self, row, col):
        self.rows[row] = col
        self.columns[col] = row
        self.leftDiagonals[row - col] = 1
        self.rightDiagonals[row + col] = 1
        self.result += self.city[row][col]

    # Undo the placement of a police
    def undoPlacement(self, row, col):
        del self.rows[row]
        del self.columns[col]
        del self.leftDiagonals[row - col]
        del self.rightDiagonals[row + col]
        self.result -= self.city[row][col]

    def storeInCompatibleGrids(self, n, x):
        i = n+1
        self.inCompatibleGrids[x] =[]
        while (i < len(self.pointsMap)):
            ((r, c), val) = self.pointsMap[i]
            if (not self.isSafe(r, c)):
                self.inCompatibleGrids[x].append(self.pointsMap[i])
                del self.pointsMap[i]
            else:
                i += 1

    def removeInCompatibleGrids(self,n, x):
        self.pointsMap += self.inCompatibleGrids[x]
        del self.inCompatibleGrids[x]
        self.pointsMap = sorted(self.pointsMap, reverse=True, key=lambda x: x[1])


    def solveWithOptimization(self, policeMenLeft, increment=0):
        if (policeMenLeft == 0):
            self.noOfSolutions += 1
            self.points.append(self.result)
            return

        while (increment < len(self.pointsMap) and policeMenLeft != 0):
            ((row, col), value) = self.pointsMap[increment]
            maxValuesPossible = sum(x[1] for x in self.pointsMap[increment+1: increment+policeMenLeft])
            isMoveValid = self.result + value + maxValuesPossible > self.currentMax()

            if (isMoveValid):
                self.placeAPolice(row, col)
                self.storeInCompatibleGrids(increment, policeMenLeft)
                self.solveWithOptimization(policeMenLeft - 1, increment + 1)
                self.removeInCompatibleGrids(increment, policeMenLeft)
                self.undoPlacement(row, col)
            increment += 1



    def solve(self):
        self.solveWithOptimization(self.noOfPolice)

    def currentMax(self):
        if (self.noOfSolutions == 0):
            return 0;
        else:
            return max(self.points)

    def returnMax(self):
        if (self.noOfSolutions == 0):
            print(0)
        else:
            print("No of solutions: {} , max: {} ".format(self.noOfSolutions, max(self.points)))


"""
Read data from the file, and create a matrix with the sum of scooter positions in each grid
"""
def initialize():
    inputFilePath = "input.txt"
    with open(inputFilePath, "r") as file:
        for cnt, line in enumerate(file):
            line = line.rstrip()
            if (cnt == 0):
                gridSize = int(line)
                matrix = np.zeros((gridSize, gridSize), dtype=np.int)
            elif (cnt == 1):
                noOfPolice = int(line)
            elif (cnt == 2):
                noOfScooters = int(line)
            else:
                x, y = map(int, line.split(","))
                matrix[x][y] += 1
    return [gridSize, noOfPolice, noOfScooters, matrix]


def main1():
    start = time.time()
    gridSize, noOfPolice, noOfScooters, matrix = initialize()
    c = CityMap(gridSize, noOfPolice, noOfScooters, matrix)
    c.createMap()
    c.solve()
    print(str(c.currentMax()))
    # f = open("output.txt","w+")
    # f.write(str(c.currentMax()) +"\n")
    # f.close()
    end = time.time()
    print "Time taken is {} s".format(str(end - start))

if __name__ == "__main__":
    main1()
