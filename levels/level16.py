from numpy import * 
import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
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
    'keke':[(6,7)],
    'bolt':[(8,5)],
    'flag':[(6,5)],
    'robot':[(8,7)],
    'pipe':(
        [(25,5),(27,8),(20,1),(20,3),(20,5),(9,15),(13,15)]
        +wallHelper(3,0,3,7)
        +wallHelper(0,1,2,1)
        +wallHelper(0,3,2,3)
        +wallHelper(0,5,2,5)
        +wallHelper(0,7,2,7)
        +wallHelper(24,0,24,5)
        +wallHelper(26,5,26,8)
        +wallHelper(22,1,23,1)
        +wallHelper(22,3,23,3)
        +wallHelper(22,5,23,5)
        +wallHelper(5,13,9,13)
        +wallHelper(9,14,13,14)
        +wallHelper(5,14,5,15)
    ),
    'lava':(
        wallHelper(15,0,15,15)
        +wallHelper(16,0,16,15)
    )
    
}

eqDict = {
    'equals':[(1,0),(1,2),(1,4),(1,6),(7,3),(7,9)],
    'and':[(10,7)],
}

effectDict = {
    'stop':[(2,0),(8,3)],
    'move':[(10,5)],
    'you':[(2,2)],
    'defeat':[(2,6)],
    'push':[(8,9)],
    'win':[(21,5)]
}

subjDict = {
    'pipeword':[(0,0)],
    'flagword':[(0,4),(2,4),(21,1)],
    'rockword':[(21,3)],
    'boltword':[(6,3)],
    'robotword':[(6,9)],
    'lavaword':[(0,6)],
    'kekeword':[(0,2)],
}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))

loadPositions(levelDict)
print('level 16 load complete, result: ', levelDict, '\n\n')
level = level(16,levelDict,
              #level size
              (28,16), 
              #background colors
              rgb(65,46,46), rgb(20,13,13),
              #top margin
              10, 
              #bgmgg
              'sounds/music/factory.ogg',
              #levelname
              'WIRELESS CONNECTION') 
