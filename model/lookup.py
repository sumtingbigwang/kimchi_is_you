import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *

#Getting players, cells, and rules ----------------------   
def getPlayer(levelDict, objects):
    players = []
    for obj in objects:
        if 'YOU' in obj.eff:
            players += [obj]
    return players
    
def getObjectsInCell(levelDict, x,y):
    position = (x,y)
    return {obj for obj, instances in levelDict.items() if position in instances}

def findObj(levelDict, tgtCell, effect): 
    #of a list of objects in a cell, this returns the object with the effect in question. 
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
    for obj in tgtObjs:
        if effect in obj.eff:
            return obj
    return None

def findClass(levelDict, tgtCell, classtype):
    tgtObjs = getObjectsInCell(levelDict,*tgtCell)
    typeCheck = classtype
    for obj in tgtObjs:
        if obj.type == typeCheck:
            return obj
    return None
            
def getEquals(wordDict):
    equals = []
    for word in wordDict:
        if isinstance(word, eq):
            equals += [word]
    return equals
                
def getObjects(level):
    objects = []
    for entry in level.dict:
        if isinstance(entry, obj):
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
        if isinstance(object, obj) and 'WIN' in object.eff:
            winCells += list(position)
    return winCells

def checkWin(app, levelDict):
    #check if any player is a win object. 
    players = app.players
    for obj in app.players:
        if 'WIN' in obj.eff:
            app.levelWin = True
    
    #check if player object is overlapping win object.
    winCells = findWin(levelDict)
    for cell in winCells:
        if findObj(levelDict, cell, 'YOU'):
            app.levelWin = True