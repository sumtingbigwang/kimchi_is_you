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
objDict = {'lava':(
    wallHelper(0,1,3,1)
    +wallHelper(0,2,1,2)
    +wallHelper(3,0,4,0)
    +[(0,3),(26,0),(11,17)]
    +wallHelper(12,16,12,17)
    +wallHelper(13,15,13,17)
    +wallHelper(14,13,14,17)
    +wallHelper(15,11,15,17)
    +wallHelper(16,9,16,17)
    +wallHelper(17,6,17,17)
    +wallHelper(18,3,18,15)
    +wallHelper(19,1,19,13)
    +wallHelper(20,0,20,12)
    +wallHelper(21,0,21,10)
    +wallHelper(22,0,22,9)
    +wallHelper(23,0,23,6)
    +wallHelper(24,0,24,3)
    +wallHelper(25,0,25,1)
),
    'wall':(
        wallHelper(6,0,6,7)
        +wallHelper(7,6,12,6)
        +wallHelper(16,0,16,3)
        +wallHelper(13,3,15,3)
        +wallHelper(12,2,12,4)
        +wallHelper(7,12,7,15)
        +wallHelper(8,13,10,13)
        +wallHelper(8,15,10,15)
        +[(12,0),(11,4),(7,4),(8,7),(12,0)]
    ),
    'kimchi':[(14,1)],
    'rock':[(12,5)],
    'flag':[(26,12)],
}

eqDict = {
    'equals':[(26,14),(9,3),(7,8),(9,12),(9,14),(1,0)]
    }

effectDict = {
    'hot':[(10,14)],
    'melt':[(10,12)],
    'stop':[(2,0)],
    'you':[(10,3)],
    'win':[(27,14)],
    'push':[(7,9)],
              }

subjDict = {
    'kimchiword':[(8,3),(8,12)],
    'rockword':[(7,7)],
    'flagword':[(25,14)],
    'wallword':[(0,0)],
    'lavaword':[(12,10),(8,14)]
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
print('level 6 load complete, result: ', levelDict, '\n\n')
level = level(6,levelDict,
              #level size
              (33,18), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/cave.ogg',
              #levelname
              'VOLCANO') 
