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
        [(18,13),(19,15),
         (15,1),(13,4),(12,4),
         (12,5),(16,5),(16,8)]
        +wallHelper(9,6,9,16)
        +wallHelper(10,16,19,16)
        +wallHelper(18,14,23,14)
        +wallHelper(22,13,24,13)
        +wallHelper(24,3,24,12)
        +wallHelper(21,3,23,3)
        +wallHelper(18,4,21,4)
        +wallHelper(18,5,19,5)
        +wallHelper(16,3,18,3)
        +wallHelper(16,1,16,2)
        +wallHelper(14,1,14,4)
        +wallHelper(10,6,14,6)
        +wallHelper(14,7,14,8)
        +wallHelper(16,7,19,7)
        +wallHelper(19,8,23,8)
    ),
    'kimchi':[(17,11)],
    'flag':[(20,7)],
    'baba':[(15,11)]
    }

eqDict = {
    'equals':[(11,2),(10,5),(22,6),
              (20,13),(21,15),(11,10),
              (14,5)],
    'not':[(22,15)],
}

effectDict = {
    'you':[(21,13),(23,15)],
    'win':[(22,7),(19,11)],
    'stop':[(12,2)],
    'defeat':[(15,6)],
    'move':[(14,13)],
    'push':[(11,11)]
}

subjDict = {
    'kimchiword':[(19,13)],
    'flagword':[(21,5),(19,10)],
    'babaword':[(20,15),(9,5),(11,5),(11,9)],
    'wallword':[(10,2)],
    'level':[(13,5)],
    
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
print('level 22 load complete, result: ', levelDict, '\n\n')
level = level(22,levelDict,
              #level size
              (33,18), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'METAMETA(HOSTILE ENVIRONMENT)')