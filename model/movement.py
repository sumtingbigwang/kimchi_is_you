from model.lookup import *
from cmu_graphics import *
import sys, time
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.rules import *

#move dictionary (to save space)
moveDict = {'right': (1,0), 'left':(-1,0), 'up':(0,-1),'down':(0,1)}

#move and push mechanic--------------------------------------
def movePlayers(app, levelDict, players, move):
    for player in players:
        moveObj(app,levelDict,player,move)
        
#old key hold move function (funky)
def moveLoop(app, levelDict, players, move):
    while app.moveLoop:
        time.sleep(0.1)
        movePlayers(app, levelDict, players, move)
    
#turns out cursor is dogshit at debugging anything that isn't a simple bug! :)
#had to redo much of this myself later anyway.

def moveObj(app, levelDict, obj, move):
    #get target cell coords
    x, y = obj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    
    #legality check
    if not isLegal(levelDict, tgtCell, obj):
        if app.debugMode:
            print(obj.name,'move illegal')
            targetObjs = getObjectsInCell(levelDict, *tgtCell)
            for obj in targetObjs:
                print(obj.effectsList)
        obj.changeDir(move)
        return None
    
    #get tgt objs
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    #target cell is nonempty
    if tgtObjs and 'float' not in obj.effectsList and obj.attribute != 'cursor':
        #test each object in target cell for collision
        for tgtObject in tgtObjs:
            if (('you' in tgtObject.effectsList and 'stop' in tgtObject.effectsList) or 
                ('you' in tgtObject.effectsList and 'push' in tgtObject.effectsList)):
                #this is another instance of you, which we only need check for movement space. 
                if pushableObj(app, levelDict, tgtObject, move) is None:
                    if app.debugMode:
                       print(obj.name,'cannot push')
                    obj.changeDir(move)
                    return None
            elif 'push' in tgtObject.effectsList:
                #pushable object, begin recursion. 
                #for this we actually want to move the target object if it passes, not just check for pushability. 
                if pushObj(app, levelDict, tgtObject, move) is None:
                    if app.debugMode:
                        print(obj.name,'cannot push')
                    obj.changeDir(move)
                    return None #if object doesn't push, then we just break and don't move
            
            #if we get here, the pushable object is moved, and we're happy. 
    
    #recursion passed, now move our original object
    if obj in levelDict:
        del levelDict[obj] #clear the original position before writing 
    app.turnMoves.append((obj, move))
    obj.MoveObject(move)
    levelDict[obj] = obj.pos
    if app.debugMode:
        print(obj.name,'moved', obj.pos)
    return True

def pushObj(app, levelDict, object, move):
    #check if object itself can be pushed
    if pushableObj(app, levelDict, object, move) is None:
        if app.debugMode:
            print(object.name,'pushing move illegal')
        object.changeDir(move)
        return None
        
    #get the nsext cell's objects and push them first
    x, y = object.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    
    #push objects in the target cell first
    if tgtObjs:
        for tgtObj in tgtObjs:
            if 'push' in tgtObj.effectsList:
                if pushObj(app, levelDict, tgtObj, move) is None:
                    if app.debugMode:
                        print(object.name,'cannot push')
                    object.changeDir(move)
                    return None
                
    #then move this object
    if object in levelDict:
        del levelDict[object]
    object.MoveObject(move)
    levelDict[object] = object.pos
    app.turnMoves.append((object, move))
    if app.debugMode:
        print(obj.name,'moved', obj.pos)
    return True

def pushableObj(app, levelDict, obj, move):
    x, y = obj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    
    #legality check
    if not isLegal(levelDict, tgtCell, obj):
        return None
    
    #get objects, repeat shi above
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    
    if tgtObjs:
        for tgtObj in tgtObjs:
            #if target has stop and no push, and we're not a you+stop object, we can't move
            if ('stop' in tgtObj.effectsList 
                  and not ('you' in obj.effectsList and 'stop' in obj.effectsList)):
                if 'push' not in tgtObj.effectsList:
                    return None
            
            #regular push case - ALL objects in target cell must be pushable
            #'you' + 'stop' and 'you' + 'push' behave like pushable objects basically.
            elif ('push' in tgtObj.effectsList 
            or ('you' in tgtObj.effectsList and 'stop' in tgtObj.effectsList)
            or ('you' in tgtObj.effectsList and 'push' in tgtObj.effectsList)):
                if pushableObj(app, levelDict, tgtObj, move) is None:
                    return None
    return True
        
#legality checks--------------------------------------
def inBounds(x,y): 
    return (x < app.cols and x >= 0 
            and y < app.rows and y >= 0)
    
def isLegal(levelDict, tgtCell, obj):
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
    if 'float' not in obj.effectsList: #'FLOAT' effect allows clipping
        if tgtObjs != None:
            for object in tgtObjs:
                return ('stop' not in object.effectsList #object is not unpushable
                        or ('stop' in object.effectsList and 'push' in object.effectsList) 
                        #object is 'STOP', but PUSH overrides STOP
                        or ('stop' in object.effectsList and 'you' in object.effectsList))
                        #object is 'STOP', but you also are moving it
    tgtX, tgtY = tgtCell
    return inBounds(tgtX, tgtY)

#reset functions--------------------------------------
def undoMove(app):
    if len(app.moveHistory) == 0: #no moves to undo
        return None
    moveStack = app.moveHistory.pop()
    for move in moveStack:
        if len(move) == 2: #this means tuple is a move
            (object, direction) = move
            #could be better implementation for this lmao
            (object, direction) = move
            object.undoMove()
            app.levelDict[object] = object.pos
        elif len(move) == 3: #this means tuple is a type change
            (object, oldType, newType) = move
            object.setAttribute(oldType)
    
def resetLevel(app):
    #create a list of items before iterating to avoid dictionary modification during iteration
    items = list(app.levelDict.keys())
    for item in items:
        item.resetPos()
        app.levelDict[item] = item.pos
        item.attribute = item.initialState
    app.level.moveHistory = []
    app.turnMoves = []
    app.replaceCount = 0
    
    # Just update rules without checking win state
    level = app.level
    level.rules = compileRules(level)
    delRules(level)
    getRules(level)
    makeRules(app,level)
    
    # Update players
    app.players = getPlayer(app.level)
    app.noPlayer = len(app.players) == 0