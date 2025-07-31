import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *

#Getting players, cells, and rules ----------------------   
def getPlayer(app):
    players = []
    for object in app.levelDict:
        if isinstance(object, obj):
            if (('you' in object.effectsList and object not in players)
                or (object.attribute == 'cursor')):
                players += [object]
    return players

def getObjectsInCell(app, x,y):
    position = (x,y)
    return [item for item, itempos in app.levelDict.items() if itempos == position]

def findObjInCell(app, tgtCell, attribute):
    tgtObjs = getObjectsInCell(app, *tgtCell)
    for obj in tgtObjs:
        if obj.attribute == attribute:
            return obj
    return None

def findObj(app, tgtCell, effect): 
    #of a list of objects in a cell, this returns the object with the effect in question. 
    tgtObjs = getObjectsInCell(app, *tgtCell)
    for obj in tgtObjs:
        if effect in obj.effectsList:
            return obj
    return None

def findClass(app, tgtCell, classtype):
    tgtObjs = getObjectsInCell(app,*tgtCell)
    typeCheck = classtype
    for obj in tgtObjs:
        if obj.type == typeCheck:
            return obj
    return None
            
def getEquals(app):
    equals = []
    for item in app.levelDict:
        if item.type == 'eq':
            if item.attribute == 'equals':
                equals.insert(0,item)
            elif item.attribute == 'and':
                equals.insert(-2,item)
            else: #NOT operator
                equals.append(item)
    return equals
                
def getAllObjects(app):
    objects = []
    for entry in app.levelDict:
        if isinstance(entry, obj):
            objects += [entry]
    return objects
                
def getFirstObject(app, name):
    for item in app.levelDict:
        if item.attribute == name:
            return item
    return None
                
def checkstate(app):
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
    checkWin(app, app.levelDict)
    
def findWin(app):
    winCells = []
    for object, position in app.levelDict.items():
        if isinstance(object, obj) and 'win' in object.effectsList:
            winCells.append(position)
    return winCells

def checkWin(app, levelDict):
    if app.levelWin:  # If we've already won, don't check again
        return None
        
    #check if any player is a win object. 
    players = app.players
    for object in app.players:
        if 'win' in object.effectsList:
            app.levelWin = True
            print('found win! wintype = player object')
            Sound('sounds/win.mp3').play()
            return None
    
    #check if player object is overlapping win object.
    winCells = findWin(app)
    for cell in winCells:
        if (findObj(app, cell, 'you') 
            and (('float' in findObj(app, cell, 'you').effectsList
                 and 'float' in findObj(app, cell, 'win').effectsList)
            or ('float' not in findObj(app, cell, 'you').effectsList
                and 'float' not in findObj(app, cell, 'win').effectsList))):
            app.levelWin = True
            print('found win! wintype = overlap')
            Sound('sounds/win.mp3').play()
            return None

def findLookupList(app, targetAttribute):
    for searchObj in app.levelDict:
        if searchObj.attribute == targetAttribute:
            return searchObj.effectsList
    return []

def wallHelper(startX, startY, endX, endY):
    if startX == endX:
        return [(startX,i) for i in range(startY,endY+1)]
    elif startY == endY:
        return [(i,startY) for i in range(startX,endX+1)]
    else:
        return [(i,j) for i in range(startX,endX) for j in range(startY,endY)]