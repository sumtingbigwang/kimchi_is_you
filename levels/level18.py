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
    'jiji':[(11,3)],
    'lava':(wallHelper(13,5,13,8)
            +wallHelper(9,5,9,8)
            +wallHelper(10,5,12,5)
            +wallHelper(10,8,12,8)
            +wallHelper(18,12,23,12)
            +[(10,6),(18,13)]
            ),
    'rock':(
        wallHelper(0,0,5,0)
        +wallHelper(0,1,3,1)
        +wallHelper(0,2,0,3)
        +wallHelper(23,7,23,11)
        +wallHelper(22,9,22,11)
        +wallHelper(21,10,21,11)
        +wallHelper(20,0,23,0)
        +wallHelper(22,1,23,1)
    ),
    'tile':([(11,6),(12,6)]
            +wallHelper(10,7,12,7)
    ),
    'flag':[(2,10)],
    'key':[(4,10)]
}

eqDict = {
    'equals':[(8,5),(20,13)],
    'and':[(8,7),(22,13)]
}

effectDict = {
    'you':[(8,6)],
    'open':[(8,8)],
    'stop':[(21,13)],
    'shut':[(23,13)],
    'win':[(11,7)]
}

subjDict = {
    'jijiword':[(8,4)],
    'flagword':[(2,9)],
    'keyword':[(4,9)],
    'lavaword':[(19,13)],
}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))

loadPositions(levelDict)
print('level 18 load complete, result: ', levelDict, '\n\n')
level = level(18,levelDict,
              #level size
              (24,14), 
              #background colors
              rgb(65,46,46), rgb(20,13,13),
              #top margin
              10, 
              #bgmgg
              'sounds/music/cave.ogg',
              #levelname
              'TINY ISLE') 
