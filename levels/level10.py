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
'wall':(
    wallHelper(5,12,11,12)
    +wallHelper(8,10,11,10)
    +wallHelper(5,3,5,7)
    +wallHelper(9,3,9,7)
    +wallHelper(6,3,8,3)
    +[(6,7),(8,7),(5,11),(13,11)]
),
'jelly':(
    wallHelper(23,2,25,2)
    +wallHelper(23,6,25,6)
    +wallHelper(22,3,22,5)
    +wallHelper(26,3,26,5)
    +[(23,3),(25,3),(23,5),(25,5)]
),
'kimchi':[(7,5)],
'ice':(
    wallHelper(11,0,17,0)
    +wallHelper(12,1,18,1)
    +wallHelper(13,2,19,2)
    +wallHelper(13,3,20,3)
    +wallHelper(14,4,20,4)
    +wallHelper(14,5,16,5)
    +wallHelper(20,5,21,5)
    +wallHelper(14,6,15,6)
    +[(21,6),(15,7),(21,7),(21,8),(15,8),(15,9),(16,9)]
    +wallHelper(20,9,23,9)
    +wallHelper(16,10,22,10)
    +wallHelper(17,11,22,11)
    +wallHelper(18,12,21,12)
    +wallHelper(19,13,25,13)
    +wallHelper(20,14,26,14)
    +wallHelper(21,15,24,15)
),
'flag':[(24,4)]
}

eqDict = {
'equals':[(1,0),(9,11),(26,0),(26,15)],
'and':[(11,11)]
    }

effectDict = {
    'sink':[(27,0),(12,11)],
    'win':[(2,0)],
    'you':[(10,11)],
    'stop':[(27,15)]
              }

subjDict = {
    'jellyword':[(25,0)],  
    'wallword':[(25,15),(18,7)],
    'kimchiword':[(8,11)],
    'flagword':[(0,0)],
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
print('level 10 load complete, result: ', levelDict, '\n\n')
level = level(10,levelDict,
              #level size
              (28,16), 
              #background colors
              rgb(45,59,123), rgb(16,21,40),
              #top margin
              10, 
              #bgm
              'sounds/music/ruin.ogg',
              #levelname
              'ICY WATERS') 
