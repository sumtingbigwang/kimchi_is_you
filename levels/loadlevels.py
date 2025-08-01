from cmu_graphics import *
from model.objects import *
from view.loadimages import *
from view.drawgrid import *
from model.lookup import *
from model.rules import *
from levels import *
levelDict = {69: testlevel.level,
            -1: map.level,
             0: menu.level,
            1: level1.level,
             2: level2.level,
             3: level3.level,
             4: level4.level,
             5: level5.level,
             6: level6.level,
             7: level7.level,
             8: level8.level,
             9: level9.level,
             10: level10.level,
             11: level11.level,
             12: level12.level,
             13: level13.level,
             14: level14.level,
             15: level15.level,
             16: level16.level,
             17: level17.level,
             18: level18.level,
             19: level19.level,
             20: level20.level,
             21: level21.level,
             22: level22.level,
             }

def readFile(path):
    with open(path, 'r') as file:
        return int(file.read())
    
def writeFile(path, levelnum):
    with open(path, 'wt') as file:
        file.write(str(levelnum))
    
    
def loadLevel(app, levelnum):
    if app.noPlayer and not app.inMenu:
        app.deadSound.pause()
        app.noPlayer = False
    app.sound.pause()  #bgm pause
    app.level = levelDict[levelnum]
    app.levelNum = app.level.num
    app.inMap = app.level.inMap
    app.inMenu = app.level.inMenu
    if app.level.num == -1: #lets us write cursor positions to the map level dict
        app.levelDict = app.level.dict
    else:
        app.levelDict = copy.deepcopy(app.level.dict)
    app.inMenu = app.level.inMenu
    app.sound = Sound(app.level.bgm)
    app.sound.play(loop = True)
    
    #save level num for 'continue' option
    if app.levelNum != 0:
        writeFile('levels/lastPlayed.txt', app.levelNum)
    
    #initialize animation and pointer metrics 
    app.animIndex = 0
    app.pointerIdx = 0
    
    #load sprites and anims
    app.spriteDict = loadSprites(app)
    
    #define game states
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    app.giveHint = False
    app.gameWin = False
    app.wasDead = False
    app.levelDefeat = False
    app.levelHot = False
    app.wasMap = False
    
    
    #initialize level
    #make move history and turnMove sets, then get all rules from the board and define players
    app.moveHistory = []
    app.turnMoves = []
    app.levelRules = compileRules(app)
    app.checkSoundList = []
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
    