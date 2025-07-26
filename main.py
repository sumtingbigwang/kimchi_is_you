from cmu_graphics import *
from levels import * 
from view.drawinfo import *
from model.objects import * 
from model.lookup import *
from view.drawgrid import *
from view.drawobj import *
from view.drawscreens import *
from view.loadimages import *
from model.movement import * 
from model.rules import *
import copy

def onAppStart(app):
    loadSheets(app)
    
    #define window size--------
    app.initHeight = 800
    app.initWidth = 800
    app.height = app.initHeight
    app.width = app.initWidth
    
    #initialize animation metrics 
    app.animIndex = 0
    app.stepsPerSecond = 6
    
    #define level
    app.level = level1.level
    app.levelDict = (app.level).dict
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #initialize level
    # make move history and turnMove sets, then get all rules from the board and define players
    app.moveHistory = []
    app.turnMoves = []
    app.objects = getObjects(app.level)
    app.players = getPlayer(app.level)
    refresh(app, app.level)
    print(app.level.rules)
    
    #define game states
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.drawGrid = True
    
    #load level and define level size ---------
    app.rows = app.level.size[1]
    app.cols = app.level.size[0]
    

    #define empty space width --------
    app.baseHspace = 10
    app.baseVspace = 10
    
    #define grid lines---------
    app.cellBorderWidth = 1
    
    # Initialize size tracking
    app.lastWidth = app.width
    app.lastHeight = app.height
    
    # Calculate initial dimensions after all variables are set
    calculateGridDimensions(app)
    
    # Initialize board after dimensions are calculated
    app.board = [([None] * app.cols) for row in range(app.rows)]

#inputs------------------------------------
def onKeyPress(app, key):
    if app.askReset:
        if key == 'y':
            resetLevel(app)
            app.askReset = False
        elif key == 'n':
            app.askReset = False

    if app.levelWin:
        if key == 'c':
            app.levelWin = False
            app.askReset = False
            resetLevel(app)
            app.players = getPlayer(app.level) 
            checkstate(app)

    if not app.levelWin and not app.askReset:
    #on key tap inputs:
        if key == 'right':
            movePlayers(app,app.levelDict,app.players,'right')
        elif key == 'left':
            movePlayers(app,app.levelDict,app.players,'left')
        elif key == 'up':
            movePlayers(app,app.levelDict,app.players,'up')
        elif key == 'down':
            movePlayers(app,app.levelDict,app.players,'down')
        elif key == 'z':
            undoMove(app)
        elif key == 'r': #reset function
            app.askReset = True
        elif key == 'g':
            app.drawGrid = not app.drawGrid
    #check and add/remove rules based on words on the screen.
        refresh(app, app.level)
        app.players = getPlayer(app.level)
        checkstate(app)
        
def onStep(app):
    #update animations 
    app.animIndex = (app.animIndex + 1) % 3
    #check for app size changes
    if app.width != app.initWidth or app.height != app.initHeight:
        calculateGridDimensions(app)

def redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='black', opacity = 100)
    drawGame(app,app.levelDict)
    if app.drawGrid:
        drawBoard(app)
        drawBoardBorder(app)
    
    if app.askReset:
        drawResetScreen(app, 'black')
        
    if app.levelWin: #want to draw win screen on top
        drawWinScreen(app, 'black') #black is a placeholder color. 
        #Store the level color in the level class, and refer to that later
    
    if app.noPlayer:
        drawNoPlayerScreen(app, 'black')

    if not app.levelWin and not app.askReset and not app.noPlayer:
        drawLabel('Debug strings',app.width//2,25,size = 10, fill = 'white')
        drawLabel(f'Current rules: {printRules(app.level.rules)}',app.width//2,40,size = 10, fill = 'white')
    
def main():
    runApp()

main()