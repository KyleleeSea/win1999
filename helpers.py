# View Helpers
def getCellBounds(row, col, maze, app):
    width = app.width - 2*app.margin
    height = app.height - 2*app.margin
    (numRows, numCols) = (len(maze), len(maze[0]))
    cellWidth = width//numRows
    cellHeight = height//numCols
    (x0, y0, x1, y1) = (col*cellWidth, row*cellHeight, (col+1)*cellWidth,
    (row+1)*cellHeight)
    return (x0, y0, x1, y1)