from controller.keycontrols import *
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
    
    #misc settings
    app.replaceCount = 0
    
    #bgm (temporary) 
    app.sound = Sound('sounds/Baba Is You OST - Wall Is Stop - Starting off.mp3')
    app.sound.play(loop = True)
    
    #define window size--------
    app.initHeight = 800
    app.initWidth = 800
    app.height = app.initHeight
    app.width = app.initWidth
    
    #initialize animation metrics 
    app.animIndex = 0
    app.stepsPerSecond = 5.5
    app.pointerIdx = 0
    app.lastMoveTime = 0  # Track when the last move happened
    
    #define level
    app.level = menu.level
    app.levelDict = (app.level).dict
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #define game states
    app.inMenu = True
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    app.debugMode = False
    
    #initialize level
    #make move history and turnMove sets, then get all rules from the board and define players
    app.moveHistory = []
    app.turnMoves = []
    app.objects = getObjects(app.level)
    app.players = getPlayer(app.level)
    refresh(app, app.level)
    
    #load level and define level size ---------
    app.rows = app.level.size[1]
    app.cols = app.level.size[0]

    #define empty space width --------
    app.baseHspace = app.level.margin
    app.baseVspace = app.level.margin
    
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
    if app.inMenu:
        menuControls(app, key)
    else:
        gameControls(app, key)
        
def onKeyHold(app, key):
    if not app.inMenu:
        gameKeyHold(app, key)
        
def onStep(app):
    #update animations 
    app.animIndex = (app.animIndex + 1) % 3
    #check for app size changes
    if app.width != app.initWidth or app.height != app.initHeight:
        calculateGridDimensions(app)

def redrawAll(app):
    drawGame(app, app.levelDict)
    if not app.inMenu:
        if app.askReset:
            drawResetScreen(app, 'black')
            
        if app.levelWin: #want to draw win screen on top
            drawWinScreen(app, 'black') #black is a placeholder color. 
            #Store the level color in the level class, and refer to that later
        
        if app.noPlayer:
            drawNoPlayerScreen(app, 'black')

        if app.paused:
            drawPauseScreen(app, 'black')
            
    if app.debugMode:
        drawBoard(app)
        drawBoardBorder(app)
        
    if not app.levelWin and not app.askReset and not app.noPlayer:
        drawLabel('Debug strings',app.width//2,25,size = 10, fill = 'white')
        drawLabel(f'Current rules: {printRules(app.level.rules)}',app.width//2,40,size = 10, fill = 'white')
    
def main():
    runApp()

main()