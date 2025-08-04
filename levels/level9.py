from numpy import * 
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'model'))
from model.objects import * 
from model.lookup import *
from model.movement import *
from model.rules import *

#COORDINATES MUST BE OFFSET BY 1! THE LEVEL STARTS AT (0,0)!
#level initialization is stored in these dictionaries, which are not changed.
#can use these dictionaries to reset the level later. (key:value is object type : initial position) 
#refer to levelDict for the actual object position / information storage. 

levelDict = {} #levelDict starts out by being just a size dictionary. 

#then objects are introduced to be loaded. You edit the level here! 
objDict = {
'keke':[(6,3),(7,7),(12,10)],
'kimchi':[(3,5)],
'flag':[(16,7)],
'grass':(
    wallHelper(14,5,18,5)
    +wallHelper(14,9,18,9)
    +wallHelper(14,6,14,8)
    +wallHelper(18,6,18,8)
)
}

eqDict = {
    'equals':[(1,0),(10,5),(10,9),(0,12),(22,13)]
    }

effectDict = {
    'defeat':[(2,0)],
    'win':[(0,13)],
    'push':[(11,9)],
    'move':[(11,5)],
    'you':[(23,13)],
              }

subjDict = {
    'kekeword':[(9,5)],
    'kimchiword':[(21,13)],
    'flagword':[(0,11),(9,9)],
    'grassword':[(0,0)]
    }

adjDict = {} #no adjectives in this level. 

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
levelDict.update(loadAdjs(adjDict))

loadPositions(levelDict)
print('level 9 load complete, result: ', levelDict, '\n\n')
level = level(9,levelDict,
              #level size
              (24,14), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'HIRED HELP') 
