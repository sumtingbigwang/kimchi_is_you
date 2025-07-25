from model.lookup import *
from cmu_graphics import *
import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.rules import refresh

#move dictionary (to save space)
moveDict = {'right': (1,0), 'left':(-1,0), 'up':(0,-1),'down':(0,1)}

#move and push mechanic--------------------------------------
def movePlayers(app, levelDict, players, move):
    for player in players:
        moveObj(app,levelDict,player,move)
    
#Cursor AI: debugged moveObj and pushObj function from last commit.
#object position tuble wasn't being removed from levelDict, so it would glitch
#everywhere and cause hella issues. 

def moveObj(app, levelDict, obj, move, undo=False):
    #im ngl ive been working on this specific function for more than 2 hours bruh.
    #i asked claude to help debug, it works now, im leaving it the hell alone
    
    #get target cell coords
    x, y = obj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    print('moving player',x,y,dx,dy,tgtCell)
    
    #legality check
    if not isLegal(levelDict, tgtCell):
        print('move', tgtCell, 'illegal')
        return None
    
    #get tgt objs
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    
    #target cell is nonempty
    if tgtObjs:
        #test each object in target cell for collision
        for tgtObj in tgtObjs:
            if 'push' in tgtObj.effectsList:
                #pushable object, begin recursion
                if pushObj(app, levelDict, tgtObj, move) is None:
                    return None #if object doesn't push, then we just break and don't move
    
    #recursion passed, now move object
    if obj in levelDict:
        del levelDict[obj]
    app.turnMoves.append((obj, move))
    obj.MoveObject(move)
    levelDict[obj] = obj.pos
    
    return True

def pushObj(app, levelDict, obj, move):
    #get target cell coords
    x, y = obj.pos
    dx, dy = moveDict[move]
    tgtCell = (x + dx, y + dy)
    
    #legality check
    if not isLegal(levelDict, tgtCell):
        return None
    
    #get objects, repeat shi above
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    
    if tgtObjs:
        for tgtObj in tgtObjs:
            if 'push' in tgtObj.effectsList:
                if pushObj(app, levelDict, tgtObj, move) is None:
                    return None
    
    print('pushing object', obj.name, move)
    if obj in levelDict:
        del levelDict[obj]
    print('appending to history', obj.name, move)
    app.turnMoves.append((obj, move))
    obj.MoveObject(move)
    levelDict[obj] = obj.pos
    
    return True
        
#legality checks--------------------------------------
def inBounds(x,y): 
    return (x < app.cols and x >= 0 
            and y < app.rows and y >= 0)
    
def isLegal(levelDict, tgtCell):
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
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
    print('undoing:',app.level.moveHistory)
    if len(app.level.moveHistory) == 0: #no moves to undo
        return None
    moveStack = app.level.moveHistory.pop()
    for move in moveStack:
        print(move)
        if len(move) == 2: #this means tuple is a move
            (object, direction) = move
            print('undoing move')
            #could be better implementation for this lmao
            (object, direction) = move
            print(object.posHist, object.posHist[-1])
            object.undoMove()
            app.levelDict[object] = object.pos
        elif len(move) == 3: #this means tuple is a type change
            (object, oldType, newType) = move
            object.setAttribute(oldType)
    print('post undo:',app.level.moveHistory)
    
def resetLevel(app):
    for item in app.levelDict:
        item.resetPos()
        app.levelDict[item] = item.pos
    app.level.moveHistory = []
    app.turnMoves = []
    refresh(app, app.level)