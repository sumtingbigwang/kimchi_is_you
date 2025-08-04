from cmu_graphics import *
from model.lookup import *
from model.movement import *
from model.rules import * 
from model.objects import *
from levels import *
from levels.loadlevels import *
from sounds.sounds import *
import sys, os, math, time, random
#much of this doc is adjusting for the menu controls. 

def updatePointerPosition(app):
    pointer = getFirstObject(app, 'kimchi')
    pointer.direction = 'right'
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
        if app.wasMap:
            app.inMap = True
            app.wasMap = False
    elif key == 'enter':
        if app.pointerIdx == 0: #continue
            app.paused = not app.paused
        elif app.pointerIdx == 1: #restart
            app.paused = False
            app.wasPaused = True
            app.askReset = True
            app.levelGone = False
            app.levelDefeat = False
        elif app.pointerIdx == 2:
            app.settings = True #settings screen
            app.paused = False
            app.wasPaused = True
            app.levelGone = False
            app.levelDefeat = False
        elif app.pointerIdx == 3: #return to map
            if app.noPlayer:
                app.deadSound.pause()
            loadLevel(app, -1)
        elif app.pointerIdx == 4: #return to menu
            if app.noPlayer:
                app.deadSound.pause()
            loadLevel(app, 0)
        elif app.pointerIdx == 5: #hint
            app.giveHint = not app.giveHint
        
    # Handle wrapping
    if app.pointerIdx < 0 or app.pointerIdx > 5:
        app.pointerIdx = app.pointerIdx % 6



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
    (9,11):9,
    (12,12):10,
    (13,12):11,
    (14,12):12,
    (19,12):13,
    (20,12):14,
    (21,12):15,
    (23,9):16,
    (24,9):17,
    (15,2):18,
    (14,2):19,
    (13,2):20,
    (12,2):21,
    (2,5):22
}   
    cursor = getFirstObject(app, 'cursor')
    cursorPosition = cursor.pos
    if key == 'enter':
        if cursorPosition in mapLevelLoadDict:
            map.level.dict[cursor] = cursorPosition
            Sound('sounds/levelselect.mp3').play()
            loadLevel(app, mapLevelLoadDict[cursorPosition])
        else:
            pass
    elif key == 'escape':
        app.paused = not app.paused
        app.inMap = not app.inMap
        app.wasMap = True
    if key == 'right' or key == 'd' or key == 'D':
        movePlayers(app,app.players,'right')
    elif key == 'left' or key == 'a' or key == 'A':
        movePlayers(app,app.players,'left')
    elif key == 'up' or key == 'w' or key == 'W':
        movePlayers(app,app.players,'up')
    elif key == 'down' or key == 's' or key == 'S':
        movePlayers(app,app.players,'down')
    elif key == 'z':
        undoMove(app)
    elif key == 'r': #reset function
        app.askReset = True
    if app.askReset:
        if key == 'y':
            map.level.dict = copy.deepcopy(mapforreset.level.dict)
            loadLevel(app,-1)
            app.askReset = False
            app.wasPaused = False
        elif key == 'n':
            if app.wasPaused:
                app.paused = True
            else:
                app.paused = False
            app.askReset = False
            
    if app.gameWin:
        if key == 'c':
            app.levelDict[getFirstObject(app, 'kimchi')] = (12,2)
            app.levelDict[getFirstObject(app, 'flag')] = (16,8)
            loadLevel(app, -1)
            app.gameWin = False
        
    if getFirstObject(app, 'kimchi') and getFirstObject(app, 'flag'):
        if getFirstObject(app, 'kimchi').pos == getFirstObject(app, 'flag').pos:
            app.gameWin = True
            Sound('sounds/gamewon.ogg').play()
    playRandomMoveSound()
        

def settingsControls(app, key):
    if key == 'escape':
        if app.wasPaused:
            app.settings = False
            app.paused = True
        elif app.wasMenu:
            app.inMenu = True
            app.settings = False
    elif key == 'up':
        app.latency -= 0.005
    elif key == 'down':
        app.latency += 0.005
    elif key == 'w' or key == 'W':
        app.width = 1512
        app.height = 975
        calculateGridDimensions(app)
    playRandomMoveSound()

#claude: reworked pointer mechanics to properly wrap kimchi around. 
def menuControls(app, key):
    # Initialize pointer index if not exists
    if not hasattr(app, 'pointerIdx'):
        app.pointerIdx = 0
        updatePointerPosition(app)
    elif key == 'enter':
        if app.pointerIdx == 0: #start game
            loadLevel(app, -1) #temporary, take this to the map screen
        elif app.pointerIdx == 1:
            loadLevel(app, app.lastPlayedLevel) #load the last played puzzle (make a save file?)
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
            
        #update kimchi position
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
    app.levelDict[getFirstObject(app, 'baba')] = (4,(6+2*sIdx))
    return sIdx

def selectMenu(app, key):
    if key == 'up' or key == 'w' or key == 'W':
        app.pointerIdx -= 1
    elif key == 'down' or key == 's' or key == 'S':
        app.pointerIdx += 1
    if app.pointerIdx < 0 or app.pointerIdx > 4:
        app.pointerIdx = app.pointerIdx % 4

def gameControls(app, key):
    if app.askReset:
        if key == 'y':
            if not app.wasMap:
                if app.noPlayer:
                    app.deadSound.pause()
                    app.sound.play(restart = False, loop = True)
            Sound('sounds/levelselect.mp3').play()
            resetLevel(app)
            if app.levelGone:
                app.levelGone = False
            app.askReset = False
            app.wasPaused = False
        elif key == 'n':
            if app.wasPaused:
                app.paused = True
            else:
                app.paused = False
            app.askReset = False

    if app.levelWin:
        if app.noPlayer:
            app.deadSound.pause()
            app.noPlayer = False
        if key == 'c':
            resetLevel(app)
            app.levelWin = False
            app.askReset = False
            loadLevel(app, -1)
            app.players = getPlayer(app)
            
    if not app.levelWin and not app.askReset and not app.paused:
        #on key tap inputs:
        if key in ['right', 'd', 'D', 
                   'left', 'a', 'A', 
                   'up', 'w', 'W', 
                   'down', 's', 'S', 'space']:
            if not app.noPlayer:
                playRandomMoveSound()
            if key == 'right' or key == 'd' or key == 'D':
                movePlayers(app,app.players,'right')
            elif key == 'left' or key == 'a' or key == 'A':
                movePlayers(app,app.players,'left')
            elif key == 'up' or key == 'w' or key == 'W':
                movePlayers(app,app.players,'up')
            elif key == 'down' or key == 's' or key == 'S':
                movePlayers(app,app.players,'down')
            elif key == 'space':
                pass
            refresh(app)
            
        if key == 'z':
            if app.noPlayer:
                app.deadSound.pause()
                app.sound.play(restart = False, loop = True)
            else:
                app.sound.play(restart = False, loop = True)
            if app.levelGone:
                app.levelGone = False
            undoMove(app)
            playRandomUndoSound()

        if key == 'r': #reset function
            app.askReset = True
            
        if key == 'c':
            print(app.levelRules)
            
        if app.debugMode:
            print('\n')
            print('--------------------------------')
            print('state of board:',app.levelDict)
            print('--------------------------------')
            print('\n')
            print('history:', app.moveHistory)
            
        if app.debugMode:
            print('soundlist:', app.checkSoundList)
        #check for rule sound
        if app.checkSoundList:
            for word in app.checkSoundList: #check for rule sound
                checkRuleSound(word)
            app.checkSoundList = [] 
    if app.noPlayer:
        app.sound.pause()
        app.deadSound.play(loop = True, restart = False)
            
    #check and add/remove rules based on words on the screen.
    if key == 'escape':
        app.paused = not app.paused