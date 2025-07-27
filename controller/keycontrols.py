from model.lookup import *
from model.movement import *
from model.rules import * 
from model.objects import *
from levels import *
from levels.loadlevels import *
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

def menuControls(app, key):
    # Initialize pointer index if not exists
    if not hasattr(app, 'pointerIdx'):
        app.pointerIdx = 0
        updatePointerPosition(app)
    
    if key == 'g':
        app.debugMode = not app.debugMode
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
            
    elif key == 'p':
        loadLevel(app, 1)
    elif key == 'enter':
        pass

def select(app, key, sIdx):
    if key == 'up':
        sIdx -= 1
    elif key == 'down':
        sIdx += 1
    if sIdx < 0 or sIdx > 4:
        sIdx = sIdx % 4
    app.levelDict[getPointer(app)] = (4,(6+2*sIdx))
    print(app.levelDict)
    print(sIdx)
    return sIdx

def selectMenu(app, key):
    if key == 'up':
        app.pointerIdx -= 1
    elif key == 'down':
        app.pointerIdx += 1
    if app.pointerIdx < 0 or app.pointerIdx > 4:
        app.pointerIdx = app.pointerIdx % 4

def gameKeyHold(app, key):
    import time
    currentTime = time.time()
    # Only move if half a second has passed since last move
    if currentTime - app.lastMoveTime >= 0.5:
        if key == 'right':
            movePlayers(app, app.levelDict, app.players, 'right')
            app.lastMoveTime = currentTime
        elif key == 'left':
            movePlayers(app, app.levelDict, app.players, 'left')
            app.lastMoveTime = currentTime
        elif key == 'up':
            movePlayers(app, app.levelDict, app.players, 'up')
            app.lastMoveTime = currentTime
        elif key == 'down':
            movePlayers(app, app.levelDict, app.players, 'down')
            app.lastMoveTime = currentTime

def gameControls(app, key):
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
            
    if not app.levelWin and not app.askReset and not app.paused:
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

        if app.debugMode:
            print('moves made this turn:',app.turnMoves)
            print('state of board:',app.levelDict)
            print('history:', app.moveHistory)
            
        if not app.levelWin and not app.askReset and not app.paused:
            refresh(app, app.level)  # This already handles state checks
        
    #check and add/remove rules based on words on the screen.
    if key == 'escape':
        app.paused = not app.paused