from model.lookup import *
from cmu_graphics import *
import sys, time
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from sounds.sounds import *

#move dictionary (to save space)
moveDict = {'right': (1,0), 'left':(-1,0), 'up':(0,-1),'down':(0,1)}

#move and push mechanic--------------------------------------
def movePlayers(app, players, move):
    for player in players:
        moveObj(app, player,move)
        
#old key hold move function (funky)
def moveLoop(app, move):    
    while app.moveLoop:
        time.sleep(0.1)
        movePlayers(app, move)
    
#turns out cursor is dogshit at debugging anything that isn't a simple bug! :)
#had to redo much of this myself later anyway.

def moveObj(app, moveObj, move):
    pushWord = False
    wordObj = None
    #get target cell coords
    x, y = moveObj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    
    #legality check
    if not isLegal(app, tgtCell, moveObj):
        if app.debugMode:
            print(moveObj.name,'move illegal')
            targetObjs = getObjectsInCell(app, *tgtCell)
            for obj in targetObjs:
                print(obj.effectsList)
        moveObj.changeDir(move)
        return None
    
    #get tgt objs
    tgtObjs = getObjectsInCell(app, *tgtCell)
    #target cell is nonempty
    if tgtObjs and 'float' not in moveObj.effectsList and moveObj.attribute != 'cursor':
        #test each object in target cell for collision
        for tgtObject in tgtObjs:
            if 'shut' in tgtObject.effectsList:
                if 'open' in moveObj.effectsList:
                    continue
                else:
                    return None
            if (('you' in tgtObject.effectsList and 'stop' in tgtObject.effectsList) or 
                ('you' in tgtObject.effectsList and 'push' in tgtObject.effectsList)):
                #this is another instance of you, which we only need check for movement space. 
                if pushableObj(app, tgtObject, move) is None:
                    if app.debugMode:
                       print(moveObj.name,'cannot push')
                    moveObj.changeDir(move)
                    return None
            elif 'push' in tgtObject.effectsList:
                if isinstance(tgtObject, effect) or isinstance(tgtObject, subj) or isinstance(tgtObject, eq):
                    if not tgtObject.powered:
                        app.checkSoundList.append(tgtObject)
                #pushable object, begin recursion. 
                #for this we actually want to move the target object if it passes, not just check for pushability. 
                if pushObj(app, tgtObject, move) is None:
                    if app.debugMode:
                        print(moveObj.name,'cannot push')
                    moveObj.changeDir(move)
                    return None #if object doesn't push, then we just break and don't move
            
    #if we get here, the pushable object is moved, and we're happy. 
    #however, we now need to check whether our player is 'SINK' or 'DEFEAT' or 'MELT' on a HOT object for deletion. 
    if ('sink' in moveObj.effectsList 
        or 'defeat' in moveObj.effectsList 
        or ('hot' in moveObj.effectsList or 'melt' in moveObj.effectsList)
        or ('open' in moveObj.effectsList or 'shut' in moveObj.effectsList)):
            moveObj.preSink = (x,y)
    
    #recursion passed, now move our original object
    if moveObj in app.levelDict:
        del app.levelDict[moveObj] #clear the original position before writing 
        
    #play rule sound on move
    app.turnMoves.append((moveObj, move))
    moveObj.MoveObject(move)
    app.levelDict[moveObj] = moveObj.pos
    if app.debugMode:
        print(moveObj.name,'moved', moveObj.pos)
    return True

def pushObj(app, moveObj, move):
    #check if object itself can be pushed
    if pushableObj(app, moveObj, move) is None:
        if app.debugMode:
            print(moveObj.name,'pushing move illegal')
        moveObj.changeDir(move)
        return None
        
    #get the nsext cell's objects and push them first
    x, y = moveObj.pos
    moveObj.preSink = (x,y)
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    tgtObjs = getObjectsInCell(app, *tgtCell)
    
    
    #push objects in the target cell first
    if tgtObjs:
        for tgtObject in tgtObjs:
            if 'shut' in tgtObject.effectsList:
                if 'open' in moveObj.effectsList:
                    continue
                else:
                    return None
            if 'push' in tgtObject.effectsList:
                #check for word object for the rule sounds
                if isinstance(tgtObject, effect) or isinstance(tgtObject, subj) or isinstance(tgtObject, eq):
                    if not tgtObject.powered:
                        app.checkSoundList.append(tgtObject)
                #execute push
                if pushObj(app, tgtObject, move) is None:
                    if app.debugMode:
                        print(moveObj.attribute,'cannot push')
                    moveObj.changeDir(move)
                    return None
                #I THINK if we get here the object being pushed isn't a player 
                #so we dont need to check for DEFEAT.
            elif ('sink' in tgtObject.effectsList
                  or ('hot' in tgtObject.effectsList and 'melt' in moveObj.effectsList)
                  or ('shut' in tgtObject.effectsList and 'open' in moveObj.effectsList)):
                moveObj.preSink = (x,y)
                
    #then move this object
    if moveObj in app.levelDict:
        del app.levelDict[moveObj]
    moveObj.MoveObject(move)
    app.levelDict[moveObj] = moveObj.pos
    app.turnMoves.append((moveObj, move))
    if app.debugMode:
        print(moveObj.attribute,'moved', moveObj.pos)
    return True

def pushableObj(app, obj, move):
    x, y = obj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    
    #legality check
    if not isLegal(app, tgtCell, obj):
        return None
    
    #get objects, repeat shi above
    tgtObjs = getObjectsInCell(app, *tgtCell)
    
    if tgtObjs:
        for tgtObj in tgtObjs:
            #if target has stop and no push, and we're not a you+stop object, we can't move
            if ('stop' in tgtObj.effectsList 
                  and not ('you' in obj.effectsList and 'stop' in obj.effectsList)
                  and not ('shut' in tgtObj.effectsList or 'open' in tgtObj.effectsList)
                  and not ('you' in tgtObj.effectsList)):
                if 'push' not in tgtObj.effectsList:
                    return None
            
            #regular push case - ALL objects in target cell must be pushable
            #'you' + 'stop' and 'you' + 'push' behave like pushable objects basically.
            elif ('push' in tgtObj.effectsList 
            or ('you' in tgtObj.effectsList and 'stop' in tgtObj.effectsList)
            or ('you' in tgtObj.effectsList and 'push' in tgtObj.effectsList)):
                if pushableObj(app, tgtObj, move) is None:
                    return None
    return True
        
#legality checks--------------------------------------
def inBounds(x,y): 
    return (x < app.cols and x >= 0 
            and y < app.rows and y >= 0)
        
def isLegal(app, tgtCell, obj):
    tgtObjs = getObjectsInCell(app,*tgtCell)
    if 'float' not in obj.effectsList: #'FLOAT' effect allows clipping
        if tgtObjs != None:
            for object in tgtObjs:
                if ('stop' in object.effectsList 
                    and 'push' not in object.effectsList
                    and 'you' not in object.effectsList
                    and 'shut' not in object.effectsList):
                    return False

    tgtX, tgtY = tgtCell
    return inBounds(tgtX, tgtY)
        
def autoMoveObjs(app):
    for object in app.objects:
        if isinstance(object, obj) and 'move' in object.effectsList:
            dir = object.direction
            if not pushableObj(app, object, dir):
                if dir == 'right':
                    dir = 'left'
                elif dir == 'left':
                    dir = 'right'
                elif dir == 'up':
                    dir = 'down'
                elif dir == 'down':
                    dir = 'up'
            moveObj(app, object, dir)