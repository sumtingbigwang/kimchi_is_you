from cmu_graphics.cmu_graphics import App
from model.lookup import *
from model.movement import *
from model.rules import * 
from model.objects import *
from levels import *
from levels.loadlevels import *
import sys, math, time
#much of this doc is adjusting for the menu controls. 
#was too lazy to get the pointer going so had claude work it out
def getPointer(app):
    for item in app.levelDict:
        if item.attribute == 'baba':
            return item
    return None

def updatePointerPosition(app):
    pointer = getPointer(app)
    if pointer:
        # Update both the object position and dictionary
        newPos = (4, (6 + 2 * app.pointerIdx))
        pointer.pos = newPos
        app.levelDict[pointer] = newPos
        if app.debugMode:
            print(f"Moving pointer to {newPos}")
            
def pauseControls(app, key):
    if key in ['up', 'down', 'w', 's', 'W', 'S']:
        # Update pointer index
        if key == 'up' or key == 'w' or key == 'W':
            app.pointerIdx -= 1
        elif key == 'down' or key == 's' or key == 'S':  # down
            app.pointerIdx += 1
    elif key == 'escape':
        app.paused = not app.paused
    elif key == 'enter':
        if app.pointerIdx == 0: #continue
            app.paused = not app.paused
        elif app.pointerIdx == 1: #restart
            app.paused = False
            app.wasPaused = True
            app.askReset = True
        elif app.pointerIdx == 2:
            app.settings = True #settings screen
            app.paused = False
            app.wasPaused = True
        elif app.pointerIdx == 3: #return to map
            loadLevel(app, -1)
        elif app.pointerIdx == 4: #return to menu
            loadLevel(app, 0)
        
    # Handle wrapping
    if app.pointerIdx < 0 or app.pointerIdx > 4:
        app.pointerIdx = app.pointerIdx % 5


def mapControls(app, key):
    mapLevelLoadDict = {
    (7,13):1,
    (8,13):2,
    (9,13):3,
    (7,12):4,
    (8,12):5,
    (9,12):6,
    (7,11):7,
    (8,11):8,
    (9,11):9
}
    cursorPosition = getFirstObject(app, 'cursor').pos
    if key == 'enter':
        print(cursorPosition)
        if cursorPosition in mapLevelLoadDict:
            loadLevel(app, mapLevelLoadDict[cursorPosition])
        else:
            pass
    elif key == 'escape':
        app.paused = not app.paused
    if key == 'right' or key == 'd' or key == 'D':
        movePlayers(app,app.levelDict,app.players,'right')
    elif key == 'left' or key == 'a' or key == 'A':
        movePlayers(app,app.levelDict,app.players,'left')
    elif key == 'up' or key == 'w' or key == 'W':
        movePlayers(app,app.levelDict,app.players,'up')
    elif key == 'down' or key == 's' or key == 'S':
        movePlayers(app,app.levelDict,app.players,'down')
    elif key == 'z':
        undoMove(app)
    elif key == 'r': #reset function
        app.askReset = True
        
def settingsControls(app, key):
    if key == 'escape':
        if app.wasPaused:
            app.settings = False
            app.paused = True
        elif app.wasMenu:
            app.inMenu = True
            app.settings = False
    elif key == 'up':
        app.stepsPerSecond += 0.1
    elif key == 'down':
        app.stepsPerSecond -= 0.1
    elif key == 'w' or key == 'W':
        app.width = 800
        app.height = 800
        calculateGridDimensions(app)
        
def menuControls(app, key):
    # Initialize pointer index if not exists
    if not hasattr(app, 'pointerIdx'):
        app.pointerIdx = 0
        updatePointerPosition(app)
    elif key == 'enter':
        if app.pointerIdx == 0: #start game
            loadLevel(app, -1) #temporary, take this to the map screen
        elif app.pointerIdx == 1:
            #TEMP LOAD 
            loadLevel(app, 1) #load the last played puzzle (make a save file?)
        elif app.pointerIdx == 2:
            app.settings = True #load settings screen
            app.wasMenu = True
            app.inMenu = False
        elif app.pointerIdx == 3: #quit game
            sys.exit()
    elif key in ['up', 'down']:
        # Update pointer index
        if key == 'up':
            app.pointerIdx -= 1
        else:  # down
            app.pointerIdx += 1
        
        # Handle wrapping
        if app.pointerIdx < 0 or app.pointerIdx > 3:
            app.pointerIdx = app.pointerIdx % 4
            
        # Update Baba's position
        updatePointerPosition(app)
        if app.debugMode:
            print(f"Pointer index: {app.pointerIdx}")

def select(app, key, sIdx):
    if key == 'up' or key == 'w' or key == 'W':
        sIdx -= 1
    elif key == 'down' or key == 's' or key == 'S':
        sIdx += 1
    if sIdx < 0 or sIdx > 4:
        sIdx = sIdx % 4
    app.levelDict[getPointer(app)] = (4,(6+2*sIdx))
    print(app.levelDict)
    print(sIdx)
    return sIdx

def selectMenu(app, key):
    if key == 'up' or key == 'w' or key == 'W':
        app.pointerIdx -= 1
    elif key == 'down' or key == 's' or key == 'S':
        app.pointerIdx += 1
    if app.pointerIdx < 0 or app.pointerIdx > 4:
        app.pointerIdx = app.pointerIdx % 4

def gameKeyHold(app, keys):
    pass #the key hold function just feels weird. cmu_graphics timing is funky af
    # app.currentTime = time.time()
    # # Only move if half a second has passed since last move
    # if app.currentTime - app.lastMoveTime >= 0.18:
    #     if 'right' in keys:
    #         movePlayers(app, app.levelDict, app.players, 'right')
    #         app.lastMoveTime = app.currentTime
    #     elif 'left' in keys:
    #         movePlayers(app, app.levelDict, app.players, 'left')
    #         app.lastMoveTime = app.currentTime
    #     elif 'up' in keys:
    #         movePlayers(app, app.levelDict, app.players, 'up')
    #         app.lastMoveTime = app.currentTime
    #     elif 'down' in keys:
    #         movePlayers(app, app.levelDict, app.players, 'down')
    #         app.lastMoveTime = app.currentTime

def gameControls(app, key):
    if app.askReset:
        if key == 'y':
            resetLevel(app)
            app.askReset = False
            app.wasPaused = False
        elif key == 'n':
            if app.wasPaused:
                app.paused = True
            else:
                app.paused = False
            app.askReset = False

    if app.levelWin:
        if key == 'c':
            app.levelWin = False
            app.askReset = False
            loadLevel(app, -1)
            app.players = getPlayer(app.level)
            
    if not app.levelWin and not app.askReset and not app.paused:
        app.currentTime = time.time()
        #on key tap inputs:
        if key == 'right' or key == 'd' or key == 'D':
            movePlayers(app,app.levelDict,app.players,'right')
        elif key == 'left' or key == 'a' or key == 'A':
            movePlayers(app,app.levelDict,app.players,'left')
        elif key == 'up' or key == 'w' or key == 'W':
            movePlayers(app,app.levelDict,app.players,'up')
        elif key == 'down' or key == 's' or key == 'S':
            movePlayers(app,app.levelDict,app.players,'down')
        elif key == 'z':
            undoMove(app)
        elif key == 'r': #reset function
            app.askReset = True

        if app.debugMode:
            print('moves made this turn:',app.turnMoves)
            print('state of board:',app.levelDict)
            print('history:', app.moveHistory)
            
        if not app.levelWin and not app.askReset and not app.paused:
            refresh(app, app.level)  # This already handles state checks
        
    #check and add/remove rules based on words on the screen.
    if key == 'escape':
        app.paused = not app.paused