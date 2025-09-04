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
from model.rules import *
from model.movement import * 
from sounds.sounds import *
import copy, time
         
def onAppStart(app):
    loadSheets(app)
    startup(app)
    #misc settings
    app.replaceCount = 0
    app.levelGone = False
    app.metaMap = False
    app.gameWin = False
    app.wasDead = False
    app.levelDefeat = False
    app.levelHot = False
    
    #define key hold move timing
    app.t0 = 0 
    app.latency = 0.1
    
    #define window size--------
    app.initHeight = 975
    app.initWidth = 1512
    app.height = app.initHeight
    app.width = app.initWidth
    
    #initialize animation metrics 
    app.animIndex = 0
    app.stepsPerSecond = 5.5
    app.stepCounter = 0
    app.pointerIdx = 0
    app.lastMoveTime = 0 # Track when the last move happened
    
    #define level
    app.lastPlayedLevel = readFile('levels/lastPlayed.txt') #temporary, make a save file for this
    app.level = menu.level
    app.levelDict = copy.deepcopy((app.level).dict)
    app.levelNum = app.level.num
    app.sound = Sound(app.level.bgm)
    app.deadSound = Sound('sounds/noplayer.mp3')
    app.sound.play(loop = True, restart = True)
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #define game parameters
    app.inMenu = app.level.inMenu
    app.inMap = app.level.inMap
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    app.wasPaused = False
    app.wasMenu = False
    app.wasMap = False
    app.debugMode = False
    app.settings = False
    
    
    #initialize level
    #make move history and turnMove sets, then get all rules from the board and define players
    app.levelRules = []
    app.checkSoundList = []
    app.moveHistory = []
    app.turnMoves = []
    app.objects = getAllObjects(app)
    app.players = getPlayer(app)
    refresh(app)
    
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
        playRandomMoveSound()
    elif app.paused:
        if app.debugMode:
            print('paused')
        pauseControls(app, key)
        playRandomMoveSound()
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
    app.t0 = time.time()
    if app.levelDefeat or app.levelGone:
        playRandomDefeatSound()
    if app.levelHot:
        playRandomMeltSound()
    
def onKeyHold(app, keys):
    if not app.inMenu and not app.paused and not app.settings and not app.inMap:
        t1 = time.time()
        if t1 - app.t0 > app.latency:
            for key in keys:
                gameControls(app, key)
            app.t0 = t1
        
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
    if app.metaMap:
        app.metaMap = False
        loadLevel(app, -1)
    if app.wasDead and not app.noPlayer:
        app.deadSound.pause()
        app.sound.play(restart = False, loop = True)
        app.wasDead = False
    if not app.inMenu and not app.paused and not app.settings and not app.inMap:
        refreshRules(app)
        checkWin(app, app.levelDict)

def redrawAll(app):
    #draw map
    if app.level.inMap:
        drawRect(0,0,app.width,app.height,fill=rgb(21,24,31))
        drawMapScreen(app, app.level.background)
    drawGame(app)
    
    
    #in game screens 
    if app.levelGone:
        drawLevelExplosionScreen(app, 'black')
        
    if app.level.inMap:
        drawLevelNumbers(app)
        
    if app.settings:
        drawSettingsScreen(app)
        
    if app.gameWin:
        drawGameWinScreen(app)
        
    if not app.inMenu:
        if app.askReset:
            drawResetScreen(app, 'black')
            
        if app.levelWin: #want to draw win screen on top
            if app.inMap:
                drawGameWinScreen(app)
            else:
                drawWinScreen(app, 'black') #black is a placeholder color. 
            #Store the level color in the level class, and refer to that later
        
        if app.noPlayer and not app.inMap and not app.settings and not app.inMenu:
            drawNoPlayerScreen(app, 'black')

        if app.paused:
            drawPauseScreen(app, 'black')
    
    if app.debugMode:
        drawBoard(app)
        drawBoardBorder(app)
        
    #drawing tutorial labels
    if not app.levelWin and not app.paused:
        if app.levelNum == 1:
            drawLabel('ARROW/WASD KEYS TO MOVE',*getCellLeftTop(app, 2,8.5), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
            drawLabel('CHANGE STEPS PER SECOND IN SETTINGS!',*getCellLeftTop(app, 3,8.5), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
        elif app.levelNum == 2:
            drawLabel('(ESC) TO PAUSE',*getCellLeftTop(app, 2,2), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
            drawLabel('(Z) TO UNDO',*getCellLeftTop(app, 3,2), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
            drawLabel('(R) TO RESET',*getCellLeftTop(app, 4,2), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
        elif app.levelNum == 9:
            drawLabel('(SPACE) TO WAIT',*getCellLeftTop(app, 1,16), fill = 'white', 
                      font = 'babafont', bold = True, size = 0.5*app.cellHeight, align = 'center')
    
    if app.debugMode:
        drawLabel('DEBUG MODE ON',app.width//2,25,size = app.cellHeight*0.4, fill = 'white', font = 'babafont', bold = True)
        drawLabel(f'CURRENT RULES: {printRules(app.levelRules)}',app.width//2,40,
                  size = app.cellHeight*0.2, fill = 'white', bold = True, font = 'babafont')
    
    
def main():
    runApp()

main()