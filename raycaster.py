# https://permadi.com/1996/05/ray-casting-tutorial
# Parts from "Introduction" to "Texture Mapped Walls"
# Shoutout TA Connor Tsui for how to draw sky and ground (mini lecture)
# Shoutout TA Ben2 for explanation of finding walls at intersection vs
# naively stepping
# Shoutout Stephen Mao, discussed how to calculate height of a
# triangle. stmao@andrew.cmu.edu
from cmu_112_graphics import *
from helpers import *
import math

class Raycaster:
    def __init__(self, app, maze):
        self.maze = maze.maze
        (self.cellWidth, self.cellHeight) = getCellSpecs(app, self.maze)
        self.FOV = 60
        self.playerHeight = app.wallHeight/2

        self.numRays = 320
        self.angleBetweenRays = self.FOV/self.numRays

        self.baseWallColor = (255, 107, 107)
        self.baseSkyAndGroundColor = (255, 255, 255)
        # self.skyAndGroundColor = rgbString(255, 255, 255)
        # self.wallColor = rgbString(255, 107, 107)

    def drawMap(self, app, canvas):
        print(self.cellWidth, self.cellHeight)
        heightsWithColors = self.distsToHeights(app, canvas)
        planeWidth = app.width
        planeHeight = app.height
        cy = planeHeight/2
        currX = 0
        xAdj = planeWidth/self.numRays

        for wallSlice in heightsWithColors:
            (x0, x1) = (currX, currX+xAdj)
            self.drawWall(app, canvas, x0, x1, cy, wallSlice['projHeight'],
            wallSlice['wallColor'])
            self.drawSky(app, canvas, x0, x1, cy, wallSlice['projHeight'],
            wallSlice['skyAndGroundColor'])
            self.drawGround(app, canvas, x0, x1, cy, wallSlice['projHeight'],
            wallSlice['skyAndGroundColor'])

            currX = x1

    def drawWall(self, app, canvas, x0, x1, cy, height, color): 
        (y0, y1) = (cy-(height/2),cy+(height/2))
        currX = x1
        canvas.create_rectangle(x0,y0,x1,y1,fill=color, 
        outline=color)

    def drawSky(self, app, canvas, x0, x1, cy, height, color):
        (y0, y1) = (cy-(height/2), 0)
        canvas.create_rectangle(x0,y0,x1,y1,fill='black', 
        outline='black')

    def drawGround(self, app, canvas, x0, x1, cy, height, color):
        (y0, y1) = (cy+(height/2), app.height)
        canvas.create_rectangle(x0,y0,x1,y1,fill='black', 
        outline='black')

    def distsToHeights(self, app, canvas):
        dists = self.getDists(app, canvas)
        projHeightsWithColors = []
        distToPlane = (app.width/2)*math.tan(math.radians(30))

        for dist in dists:
            projHeight = (app.wallHeight/dist['dist'])*app.distToPlane
            projHeightsWithColors.append({'projHeight': projHeight,
            'wallColor': dist['wallColor'], 
            'skyAndGroundColor': dist['skyAndGroundColor']})
            # projectedHeights.append(projHeight)
        return projHeightsWithColors

    def getDists(self, app, canvas):
        dists = []
        angle = app.player.angle - 30
        for i in range(self.numRays):
            angle += self.angleBetweenRays
            # if statement here might be wrong. come back if bugs.
            if angle > 360:
                angle = 0
            dists.append(self.getRay(app, angle, canvas))
        return dists

    def getRay(self, app, angle, canvas):
        if angle > 90 and angle < 270:
            distHor = self.horizontalUpRay(app, angle, canvas)
        else:
            distHor = self.horizontalDownRay(app, angle, canvas)
        if angle > 0 and angle < 180:
            distVer = self.verticalRightRay(app, angle, canvas)
        else:
            distVer = self.verticalLeftRay(app, angle, canvas)
        if distHor[2] < distVer[2]:
            return {'dist': distHor[2], 'wallColor': distHor[3],
            'skyAndGroundColor': distHor[4]}
            # canvas.create_line(app.player.xPos, app.player.yPos, distHor[0], distHor[1], fill="green")        
        else:
            return {'dist': distVer[2], 'wallColor': distVer[3],
            'skyAndGroundColor': distVer[4]}
            # return {distVer[2]}
            # canvas.create_line(app.player.xPos, app.player.yPos, distVer[0], distVer[1], fill="orange")        

# rAdj and cAdj needed because intersection checks top most cell, causing
# errors in cases Vertical Left and Horizontal up. 
    def checkFirstIntersection(self, app, px, py, rAdj, cAdj):
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow+rAdj][intersectionCol+cAdj] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, 
                px, py))
        return (False, 0)

    def checkOtherIntersections(self, app, px, py, rAdj, cAdj):
        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow+rAdj][intersectionCol+cAdj] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, px, 
                py))
            # If point off map, just return a giant number 
        else:
            return (True, 10000000000000)
        return (False, 0)

    def wallShadeFormula(self, px, py, app):
        enemyToSliceDist = getDistance(px, py, app.enemy.xPos, app.enemy.yPos)
        # Getting diagonal of one quadrant
        quadrantX = (app.maze.size/2)*self.cellWidth
        quadrantY = (app.maze.size/2)*self.cellHeight
        maxDist = ((quadrantX**2 + quadrantY**2)**(1/2))
        divisor = maxDist/enemyToSliceDist
        if divisor < 1:
            divisor = 1
        elif divisor > 9:
            divisor = 9
        print(divisor)

        wallColor = []
        skyAndGroundColor = []
        for part in self.baseWallColor:
            wallColor.append(int(part/divisor))
        for part in self.baseSkyAndGroundColor:
            skyAndGroundColor.append(int(part/divisor))
        wallColor = rgbString(wallColor[0], wallColor[1], wallColor[2])
        skyAndGroundColor = rgbString(skyAndGroundColor[0], 
        skyAndGroundColor[1], skyAndGroundColor[2])
        return {'wallColor': wallColor, 'skyAndGroundColor': skyAndGroundColor}

    def verticalRightRay(self, app, angle, canvas):
    # end variable first arg: True or False condition. second arg: distance
    # value. 
        end = (False, 0)
        px = self.cellWidth*(app.player.col+1)
        py = (app.player.yPos - 
        math.tan(math.radians(angle-90))*(px-app.player.xPos))

        end = self.checkFirstIntersection(app, px, py, 0, 0)

        while end[0] != True:
            Ya = self.cellWidth*(math.tan(math.radians(angle-90)))
            px = px+self.cellWidth
            py = py-Ya
            end = self.checkOtherIntersections(app, px, py, 0, 0)

        # print(getDistance(px, py, app.enemy.xPos, app.enemy.yPos))
        colors = self.wallShadeFormula(px, py, app)
        return (px, py, end[1], colors['wallColor'], 
        colors['skyAndGroundColor'])
        # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        

    def verticalLeftRay(self, app, angle, canvas):
        end = (False, 0)
        #3.5*app.margin is a trivial fix to a bug that exists without the
        #3.5* multiplier. Revisit here if future bugs.
        px = self.cellWidth*(app.player.col)
        # print(cellWidth)
        py = (app.player.yPos - 
        math.tan(math.radians(angle-90))*(px-app.player.xPos))

        end = self.checkFirstIntersection(app, px, py, 0, -1)

        while end[0] != True:
            Ya = self.cellWidth*(math.tan(math.radians(angle-90)))
            px = px-self.cellWidth
            py = py+Ya
            end = self.checkOtherIntersections(app, px, py, 0, -1)
        # Test other intersections until hit wall

        colors = self.wallShadeFormula(px, py, app)
        return (px, py, end[1], colors['wallColor'], 
        colors['skyAndGroundColor'])        # return end[1]
        # print(end[1])
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        

    def horizontalDownRay(self, app, angle, canvas):
        end = (False, 0)
        # Horizontal
        # First intersection
        py = self.cellHeight*(app.player.row + 1)
        #0.0001 added to avoid div by 0 error
        px = (app.player.xPos + 
        (app.player.yPos - py)/(math.tan(math.radians(angle-90))
        +0.0001))

        end = self.checkFirstIntersection(app, px, py, 0, 0)

        while end[0] != True:
            Xa = self.cellHeight/((math.tan(math.radians(angle-90))
            +0.0001))
            px = px-Xa
            py = py+self.cellHeight
            end = self.checkOtherIntersections(app, px, py, 0, 0)

        colors = self.wallShadeFormula(px, py, app)
        return (px, py, end[1], colors['wallColor'], 
        colors['skyAndGroundColor'])       
         # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        

    def horizontalUpRay(self, app, angle, canvas):
        end = (False, 0)

        #1.2*app.margin is a trivial fix to a bug that exists without the
        #Revisit here if future bugs.
        # print(f'row:{app.player.row}')
        py = self.cellHeight*(app.player.row)
        #0.0001 added to avoid div by 0 error
        px = (app.player.xPos + 
        (app.player.yPos - py)/(math.tan(math.radians(angle-90))
        +0.0001))

        end = self.checkFirstIntersection(app, px, py, -1, 0)

        # Test other intersections until hit wall
        while end[0] != True:
            Xa = (self.cellHeight/(math.tan(math.radians(angle-90))
            +0.0001))
            px = px+Xa
            py = py-self.cellHeight
            end = self.checkOtherIntersections(app, px, py, -1, 0)

        colors = self.wallShadeFormula(px, py, app)
        return (px, py, end[1], colors['wallColor'], 
        colors['skyAndGroundColor'])        # return end[1]
        # canvas.create_oval(px-5,py-5,px+5,py+5,fill='green')
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        

    def redraw(self, app, canvas):
        self.drawMap(app, canvas)
        # self.getDists(app, canvas)
        # print(app.player.angle)