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
    'kimchi':[(3,3)],
    'wall':(
        wallHelper(5,0,9,0)
        +wallHelper(0,6,3,6)
        +wallHelper(11,6,14,6)
        +[(3,7),(11,7)]
    ),
    'flag':[(7,3)],
    'algae':[(1,2),(13,0),(14,1),(4,7)]
}

eqDict = {
    'equals':[(7,1),(13,7),(14,4),(1,7),(7,5)]
    }

effectDict = {
'you':[(2,7)],
'win':[(14,7)],
'stop':[(14,5)],
              }

subjDict = {
    'kimchiword':[(0,7)],
    'flagword':[(6,5),(12,7)],
    'rockword':[(6,1),(8,1),(8,5)],
    'wallword':[(14,3)]
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
print('level 11 load complete, result: ', levelDict, '\n\n')
level = level(11,levelDict,
              #level size
              (15,8), 
              #background colors
              rgb(45,59,123), rgb(16,21,40),
              #top margin
              10, 
              #bgm
              'sounds/music/ruin.ogg',
              #levelname
              'CHANGELESS') 
