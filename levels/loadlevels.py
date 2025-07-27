from cmu_graphics import *
from model.objects import *
from view.loadimages import *
from view.drawgrid import *
from model.lookup import *
from levels import *

levelDict = {1: level1.level,
             0: menu.level,
             -1: map.level}

def loadLevel(app, levelnum):
    app.sound.pause()
    #bgm 
    app.level = levelDict[levelnum]
    app.levelNum = app.level.num
    app.levelDict = (app.level).dict
    app.inMenu = app.level.inMenu
    app.sound = Sound(app.level.bgm)
    app.sound.play(loop = True)
    
    #initialize animation metrics 
    app.animIndex = 0
    app.stepsPerSecond = 5.5
    app.pointerIdx = 0
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #define game states
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    
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