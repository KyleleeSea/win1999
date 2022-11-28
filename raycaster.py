from helpers import *
from spriteCaster import *
import math

class Raycaster:
    def __init__(self, app, maze):
        self.maze = maze.maze
        (self.cellWidth, self.cellHeight) = getCellSpecs(app, self.maze)
        self.FOV = 60
        self.playerHeight = app.wallHeight/2
        self.numRays = 320
        self.angleBetweenRays = self.FOV/self.numRays
        self.skyAndGroundColor = rgbString(165, 169, 166)
        self.wallColor = rgbString(234, 107, 107)

        self.spriteInSight = False

    def testFunc(self, app):
        self.spriteInSight = False
        heights = self.distsToHeights(app)

    def drawMap(self, app, canvas):
        # self.spriteInSight = False
        heights = self.distsToHeights(app)
        planeWidth = app.width
        planeHeight = app.height
        cy = planeHeight/2
        currX = 0
        xAdj = planeWidth/self.numRays
        for height in heights:
            (x0, x1) = (currX, currX+xAdj)
            self.drawWall(app, canvas, x0, x1, cy, height)
            self.drawSky(app, canvas, x0, x1, cy, height)
            self.drawGround(app, canvas, x0, x1, cy, height)
            currX = x1

    def drawWall(self, app, canvas, x0, x1, cy, height):
        (y0, y1) = (cy-(height/2),cy+(height/2))
        currX = x1
        canvas.create_rectangle(x0,y0,x1,y1,fill=self.wallColor, 
        outline=self.wallColor )
    def drawSky(self, app, canvas, x0, x1, cy, height):
        (y0, y1) = (cy-(height/2), 0)
        canvas.create_rectangle(x0,y0,x1,y1,fill=self.skyAndGroundColor, 
        outline=self.skyAndGroundColor)
    def drawGround(self, app, canvas, x0, x1, cy, height):
        (y0, y1) = (cy+(height/2), app.height)
        canvas.create_rectangle(x0,y0,x1,y1,fill=self.skyAndGroundColor, 
        outline=self.skyAndGroundColor)
    def distsToHeights(self, app):
        dists = self.getDists(app)
        projectedHeights = []
        distToPlane = (app.width/2)*math.tan(math.radians(30))
        for dist in dists:
            projHeight = (app.wallHeight/dist)*app.distToPlane
            projectedHeights.append(projHeight)
        return projectedHeights

    def getDists(self, app):
        dists = []
        angle = app.player.angle - 30
        for i in range(self.numRays):
            angle += self.angleBetweenRays
            # if statement here might be wrong. come back if bugs.
            if angle > 360:
                angle = 0
            dists.append(self.getRay(app, angle))
        return dists

    def getRay(self, app, angle):
        if angle > 90 and angle < 270:
            distHor = self.horizontalUpRay(app, angle)
        else:
            distHor = self.horizontalDownRay(app, angle)
        if angle > 0 and angle < 180:
            distVer = self.verticalRightRay(app, angle)
        else:
            distVer = self.verticalLeftRay(app, angle)
        if distHor[2] < distVer[2]:
            if distHor[3] == True:
                self.spriteInSight = True
            return distHor[2]
            # canvas.create_line(app.player.xPos, app.player.yPos, distHor[0], distHor[1], fill="green")        
        else:
            if distVer[3] == True:
                self.spriteInSight = True
            return distVer[2]
            # canvas.create_line(app.player.xPos, app.player.yPos, distVer[0], distVer[1], fill="orange")        
# rAdj and cAdj needed because intersection checks top most cell, causing
# errors in cases Vertical Left and Horizontal up. 
    def checkFirstIntersection(self, app, px, py, rAdj, cAdj):
        if checkSpriteInSight(app, px, py, rAdj, cAdj):
            spriteInSight = True
        else:
            spriteInSight = False

        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # app.checkedCells.add((intersectionRow, intersectionCol))
        # Only check if point on map
        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
        intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow+rAdj][intersectionCol+cAdj] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, 
                px, py), spriteInSight)
        return (False, 0, spriteInSight)

    def checkOtherIntersections(self, app, px, py, rAdj, cAdj):
        if checkSpriteInSight(app, px, py, rAdj, cAdj):
            spriteInSight = True
        else:
            spriteInSight = False

        (intersectionRow, intersectionCol) = getCell(app, px, py, self.maze)
        # app.checkedCells.add((intersectionRow, intersectionCol))

        if (intersectionRow >= 0 and intersectionRow < len(self.maze) and 
            intersectionCol >= 0 and intersectionCol < len(self.maze)):
            if self.maze[intersectionRow+rAdj][intersectionCol+cAdj] == 1:
                return (True, getDistance(app.player.xPos, app.player.yPos, px, 
                py), spriteInSight)
            # If point off map, just return a giant number 
        else:
            return (True, 10000000000000, spriteInSight)
        return (False, 0, spriteInSight)
    
    def verticalRightRay(self, app, angle):
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
        return (px, py, end[1], end[2])
        # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        
    def verticalLeftRay(self, app, angle):
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
        return (px, py, end[1] , end[2])
        # return end[1]
        # print(end[1])
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="green")        
    def horizontalDownRay(self, app, angle):
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
        return (px, py, end[1], end[2])
        # return end[1]
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        
    def horizontalUpRay(self, app, angle):
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
        return (px, py, end[1], end[2])
        # return end[1]
        # canvas.create_oval(px-5,py-5,px+5,py+5,fill='green')
        # canvas.create_line(app.player.xPos, app.player.yPos, px, py, fill="orange")        
    def redraw(self, app, canvas):
        pass
        self.drawMap(app, canvas)
        # self.getDists(app, canvas)
        # print(app.player.angle)
        # self.getRay(app, app.player.angle, canvas)
        # self.getRay(app, app.player.angle, canvas)

    def timerFired(self, app):
        # app.checkedCells = set()
        # self.testFunc(app)
        app.enemyIsVisible = False
        app.enemyIsVisible = self.spriteInSight