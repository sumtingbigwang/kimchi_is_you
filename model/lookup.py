import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *

#Getting players, cells, and rules ----------------------   
def getPlayer(level):
    players = []
    for object in level.dict:
        if isinstance(object, obj):
            if 'you' in object.effectsList and object not in players:
                players += [object]
    return players
    
def getObjectsInCell(levelDict, x,y):
    position = (x,y)
    return [obj for obj, objpos in levelDict.items() if position == objpos]

def findObj(levelDict, tgtCell, effect): 
    #of a list of objects in a cell, this returns the object with the effect in question. 
    tgtObjs = getObjectsInCell(levelDict, *tgtCell)
    for obj in tgtObjs:
        if effect in obj.effectsList:
            return obj
    return None

def findClass(levelDict, tgtCell, classtype):
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
    typeCheck = classtype
    for obj in tgtObjs:
        if obj.type == typeCheck:
            return obj
    return None
            
def getEquals(levelDict):
    equals = []
    for item in levelDict:
        if item.attribute == 'equals':
            equals += [item]
    return equals
                
def getObjects(level):
    objects = []
    for entry in level.dict:
        if entry != 'size' and isinstance(entry, obj):
            objects += [entry]
    return objects
                
def checkstate(app):
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
    checkWin(app, app.levelDict)
    
def findWin(levelDict):
    winCells = []
    for object, position in levelDict.items():
        if isinstance(object, obj) and 'win' in object.effectsList:
            winCells.append(position)
    return winCells

def checkWin(app, levelDict):
    if app.levelWin:  # If we've already won, don't check again
        return None
        
    #check if any player is a win object. 
    players = app.players
    for obj in app.players:
        if 'win' in obj.effectsList:
            app.levelWin = True
            print('found win! wintype = player object')
            return None
    
    #check if player object is overlapping win object.
    winCells = findWin(app.levelDict)
    for cell in winCells:
        if findObj(levelDict, cell, 'you'):
            app.levelWin = True
            print('found win! wintype = overlap')
            return None

def findLookupList(levelDict, obj):
    for obj in levelDict:
        if obj.attribute == obj:
            return obj.effectsList
    return []