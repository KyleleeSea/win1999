# View Helpers
def getCellSpecs(app, maze):
    return (app.cellWidth, app.cellHeight)
    width = app.width
    height = app.height
    (numRows, numCols) = (len(maze), len(maze[0]))
    cellWidth = width//numRows
    cellHeight = height//numCols
    return (cellWidth, cellHeight)

def getCellBounds(row, col, maze, app):
    (cellWidth, cellHeight) = getCellSpecs(app, maze)
    (x0, y0, x1, y1) = (col*cellWidth, row*cellHeight, (col+1)*cellWidth,
    (row+1)*cellHeight)
    return (x0, y0, x1, y1)

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
def getCell(app, x, y, maze):
    row = int((y) / app.cellHeight)
    col = int((x) / app.cellWidth)

    return (row, col)

#https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'

# Dynamic audio helpers

def getDistance(x0, y0, x1, y1):
    return ((x1-x0)**2 + (y1-y0)**2)**(1/2)