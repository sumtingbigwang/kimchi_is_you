from model.lookup import *
from cmu_graphics import *
import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from enum import Enum

#move dictionary (to save space)
moveDict = {'right': (1,0), 'left':(-1,0), 'up':(0,-1),'down':(0,1)}

#move and push mechanic--------------------------------------

def movePlayers(app, levelDict, players, move):
    for player in players:
        moveObj(app,levelDict,player,move)
        

def moveObj(app, levelDict, obj, move):
    (x,y) = moveDict[move]
    posList = levelDict[obj]
    
    #first pass: identify which instances can move
    validMoves = set()
    
    for pos in posList:
        startX, startY = pos
        tgtCell = (startX + x, startY + y)
        canMove = True
        
        #check bounds / stop object case
        if not isLegal(levelDict, tgtCell):
            canMove = False
            
        else:
            #check if target cell has objects
            tgtObjs = getObjectsInCell(levelDict, *tgtCell)
            if tgtObjs:
                pushableObj = findObj(levelDict, tgtCell, 'PUSH')
                youObj = findObj(levelDict, tgtCell, 'YOU')
                if pushableObj == None and youObj == None:
                    pass  #we hit something with no collision
                elif youObj:
                    if 'STOP' in youObj.eff:
                        if not canPushObj(app, levelDict, youObj, *tgtCell, move):
                            canMove = False
                    else:
                        pass
                elif pushableObj: #we hit pushable object, begin recursion
                    if not canPushObj(app, levelDict, pushableObj, *tgtCell, move):
                        canMove = False  #push chain fails
        
        if canMove:
            validMoves.add(pos)
    
    #if no objects can move, return False
    if not validMoves:
        return False
    
    #second pass: perform moves for valid instances only
    if x == 1 or y == 1:
        validMoves = reversed(sorted(validMoves))
    else:
        validMoves = sorted(validMoves)
    for pos in validMoves:
        startX, startY = pos
        tgtCell = (startX + x, startY + y)
        
        #if target cell needs a push, push object in target cell
        pushableObj = findObj(levelDict, tgtCell, 'PUSH')
        if pushableObj:
            pushObj(app, levelDict, pushableObj, *tgtCell, move)
        
        #update the position for this instance
        posList.remove(pos)
        posList.add(tgtCell)
        changeDir(obj, move)
    return True


def canPushObj(app, levelDict, obj, startX, startY, move):
    (x,y) = moveDict[move]
    #define cells for lookup
    startCell = (startX, startY)
    tgtCell = (startX + x, startY + y)
    
    #check move legality
    if not isLegal(levelDict, tgtCell):
        return False  
    
    #get target cell objects
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    if not tgtObjs:  #empty space
        return True

    #2 cases for being able to move:   
    #either we are next to a 'YOU' object, or we are next to a pushable object. 
    pushableObj = findObj(levelDict, tgtCell, 'PUSH')
    youObj = findObj(levelDict, tgtCell, 'YOU')
    
    #object is a 'YOU' player sprite
    if youObj:
        if 'STOP' in youObj.eff or 'PUSH' in youObj.eff: 
            #want it such that 'YOU' + 'STOP' behaves like 'PUSH'
            return canPushObj(app, levelDict, youObj, *tgtCell, move)
        else: 
            #multiple player sprites with no collision can overlap
            return True
    
    #handle 'PUSH' objects
    if pushableObj == False:
        return False  #something unpushable blocking
    elif pushableObj == None: #hit object with no collision
        return True
    else: #recursively check if the chain can be pushed
        return canPushObj(app, levelDict, pushableObj, *tgtCell, move)

def pushObj(app, levelDict, obj, startX, startY,move):
    (x,y) = moveDict[move]
    startCell = (startX, startY) 
    tgtCell = (startX + x, startY + y)
    
    if not isLegal(levelDict, tgtCell):
        return False  #legality check
    
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    if tgtObjs:  #something in target cell
        
        #repeat what we did for canPushObj
        pushableObj = findObj(levelDict, tgtCell, 'PUSH')
        youObj = findObj(levelDict, tgtCell, 'YOU')
        
        if pushableObj:
            if not pushObj(app, levelDict, pushableObj, *tgtCell, move):
                return False  #chain push failed
        elif youObj:
            if 'STOP' in youObj.eff:
                #push YOU object that has STOP
                if not pushObj(app, levelDict, youObj, *tgtCell, move):
                    return False
            
    #now move the object
    levelDict[obj].remove(startCell)
    levelDict[obj].add(tgtCell)
    changeDir(obj, move)
    return True   
            
def changeDir(obj, move):
    obj.dir = move
        
#checking move / cell search legality
def inBounds(x,y): 
    return (x < app.cols and x >= 0 
            and y < app.rows and y >= 0)
    
def isLegal(levelDict, tgtCell):
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
    if tgtObjs != None:
        for obj in tgtObjs:
            return ('STOP' not in obj.eff #object is not unpushable
                    or ('STOP' in obj.eff and 'PUSH' in obj.eff) 
                    #object is 'STOP', but PUSH overrides STOP
                    or ('STOP' in obj.eff and 'YOU' in obj.eff))
                    #object is 'STOP', but you also are moving it
            
    tgtX, tgtY = tgtCell
    return inBounds(tgtX, tgtY)