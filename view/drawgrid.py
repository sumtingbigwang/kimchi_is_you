from cmu_graphics import * 

def calculateGridDimensions(app):
    """Calculate grid dimensions maintaining square cells and original ratios"""
    
    # Calculate available space for the grid in current window
    availableWidth = app.width - (2 * app.baseHspace)
    availableHeight = app.height - (2 * app.baseVspace)
    
    # Calculate what cell size would fit in each dimension
    cellSizeFromWidth = availableWidth / app.cols
    cellSizeFromHeight = availableHeight / app.rows
    
    # Use the smaller cell size to ensure grid fits and cells stay square
    app.cellSize = min(cellSizeFromWidth, cellSizeFromHeight)
    app.cellHeight = app.cellSize
    app.cellWidth = app.cellSize
    
    # Calculate actual grid dimensions
    totalGridWidth = app.cols * app.cellSize
    totalGridHeight = app.rows * app.cellSize
    
    # Center the grid in the window
    app.hspace = (app.width - totalGridWidth) / 2
    app.vspace = (app.height - totalGridHeight) / 2
    
    # Update board dimensions
    app.boardLeft = app.hspace
    app.boardTop = app.vspace
    app.boardWidth = totalGridWidth
    app.boardHeight = totalGridHeight
   
def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])

def drawBoardBorder(app):
    # draw the board outline (with double-thickness):
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill=None, border='grey',
             borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='grey',
             borderWidth=app.cellBorderWidth)

def getCellSize(app):
    return (app.cellSize, app.cellSize)

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellSize
    cellTop = app.boardTop + row * app.cellSize
    return (cellLeft, cellTop)

def resizeBoard(app, numRows, numCols, boardSize):
    app.rows = numRows
    app.cols = numCols
    app.boardLeft, app.boardWidth, app.boardHeight = boardSize
    app.board = [([None] * app.cols) for row in range(app.rows)]
    calculateGridDimensions(app)