from cmu_graphics import *
from model.objects import * 
from leveldata import *
from view.drawgrid import *
from view.drawobj import *
from model.lookup import *
from model.movement import * 
from model.rules import *
import copy

def onAppStart(app):
    #define window size--------
    app.initHeight = 800
    app.initWidth = 800
    app.height = app.initHeight
    app.width = app.initWidth
    
    #define level
    app.level = level1
    app.levelDict = (app.level).dict
    
    #get all rules from the board and then define player
    refreshRules(app.level)
    app.objects = getObjects(app.level)
    app.players = getPlayer(app.levelDict,app.objects)
    
    #define "game over" states
    app.noPlayer = False
    app.levelWin = False
    
    #load level and define level size ---------
    app.rows = app.levelDict['size'][1]
    app.cols = app.levelDict['size'][0]

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
    if not app.levelWin:
    #on key tap inputs:
        if key == 'right':
            movePlayers(app,app.levelDict,app.players,'right')
        elif key == 'left':
            movePlayers(app,app.levelDict,app.players,'left')
        elif key == 'up':
            movePlayers(app,app.levelDict,app.players,'up')
        elif key == 'down':
            movePlayers(app,app.levelDict,app.players,'down')
    if key == 'r': #reset function
        resetLevel(app)
         
    #check and add/remove rules based on words on the screen. 
    refreshRules(app.level)
    app.players = getPlayer(app.levelDict, app.objects) 
    checkstate(app)

def onStep(app):
    #check for app size changes
    if app.width != app.initWidth or app.height != app.initHeight:
        calculateGridDimensions(app)

def redrawAll(app):
    drawGame(app,app.levelDict)
    drawBoard(app)
    drawBoardBorder(app)
    if app.levelWin: #want to draw win screen on top
        drawWinScreen(app, 'black') #black is a placeholder color. 
        #Store the level color in the level class, and refer to that later
    
    drawLabel('Debug strings',app.width//2,25,size = 10)
    drawLabel(f'Current rules: {app.level.rules}',app.width//2,40,size = 10)
    
def main():
    runApp()

main()