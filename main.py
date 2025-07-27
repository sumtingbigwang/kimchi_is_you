from re import S
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
import copy, sys

def onAppStart(app):
    loadSheets(app)
    
    #misc settings
    app.replaceCount = 0
    
    #define window size--------
    app.initHeight = 800
    app.initWidth = 800
    app.height = app.initHeight
    app.width = app.initWidth
    
    #initialize animation metrics 
    app.animIndex = 0
    app.stepsPerSecond = 5.5
    app.stepCounter = 0
    app.pointerIdx = 0
    app.lastMoveTime = 0  # Track when the last move happened
    
    #define level
    app.level = menu.level
    app.levelDict = (app.level).dict
    app.levelNum = app.level.num
    app.sound = Sound(app.level.bgm)
    app.sound.play(loop = True)
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #define game states
    app.inMenu = app.level.inMenu
    app.inMap = app.level.inMap
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    app.wasPaused = False
    app.wasMenu = False
    app.debugMode = False
    app.settings = False
    
    #initialize level
    #make move history and turnMove sets, then get all rules from the board and define players
    app.moveHistory = []
    app.turnMoves = []
    app.objects = getAllObjects(app.level)
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
        if app.debugMode:
            print('in menu')
        menuControls(app, key)
    elif app.paused:
        if app.debugMode:
            print('paused')
        pauseControls(app, key)
    elif app.settings:
        if app.debugMode:
            print('settings')
        settingsControls(app, key)
    elif app.inMap:
        if app.debugMode:
            print('map')
        mapControls(app, key)
    else:
        if app.debugMode:
            print('game')
        gameControls(app, key)
    if key == 'g':
        app.debugMode = not app.debugMode
        
def onKeyHold(app, keys):
    if not app.inMenu:
        gameKeyHold(app, keys)
        
def onStep(app):
    #for extra timing; reset this counter to prevent excess memory consumption
    app.stepCounter += 1
    if app.stepCounter > 100000:
        app.stepCounter = 0
    #update animations 
    app.animIndex = (app.animIndex + 1) % 3
    #check for app size changes
    if app.width != app.initWidth or app.height != app.initHeight:
        calculateGridDimensions(app) 

def redrawAll(app):
    if app.level.inMap:
        drawRect(0,0,app.width,app.height,fill=rgb(21,24,31))
        drawMapScreen(app, app.level.background)
    drawGame(app, app.levelDict)
    
    if app.level.inMap:
        drawLevelNumbers(app)
    if app.settings:
        drawSettingsScreen(app)
        
    if not app.inMenu:
        if app.askReset:
            drawResetScreen(app, 'black')
            
        if app.levelWin: #want to draw win screen on top
            drawWinScreen(app, 'black') #black is a placeholder color. 
            #Store the level color in the level class, and refer to that later
        
        if app.noPlayer and not app.inMap and not app.settings and not app.inMenu:
            drawNoPlayerScreen(app, 'black')

        if app.paused:
            drawPauseScreen(app, 'black')
    
            
    if app.debugMode:
        drawBoard(app)
        drawBoardBorder(app)
        
    if app.debugMode:
        drawLabel('DEBUG MODE ON',app.width//2,25,size = app.cellHeight*0.4, fill = 'white', font = 'babafont', bold = True)
        drawLabel(f'CURRENT RULES: {printRules(app.level.rules)}',app.width//2,40,
                  size = app.cellHeight*0.2, fill = 'white', bold = True, font = 'babafont')
    
def main():
    runApp()

main()