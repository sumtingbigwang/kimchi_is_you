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
    'wall':(
        wallHelper(8,5,8,14)
        +wallHelper(9,14,19,14)
        +wallHelper(19,5,19,13)
        +wallHelper(15,5,18,5)
        +wallHelper(9,5,13,5)
        +wallHelper(24,0,24,3)
        +wallHelper(25,3,25,4)
        +wallHelper(26,3,26,7)
        +wallHelper(27,7,27,9)
        +wallHelper(25,1,27,1)
        +wallHelper(22,0,23,0)
        +wallHelper(22,2,23,2)
        +wallHelper(22,2,22,3)
        +[(21,3),(17,7),(2,3)]
        +wallHelper(0,3,0,6)
        +wallHelper(1,3,1,4)
        +wallHelper(3,0,3,3)
        +wallHelper(0,1,2,1)
        +wallHelper(4,0,4,1)
        +wallHelper(5,0,6,0)
    ),
    'door':[(14,5)],
    'key':[(11,9)],
    'robot':[(16,9)],
    'algae':(
        wallHelper(16,15,21,15)
        +wallHelper(19,0,20,0)
        +wallHelper(26,0,27,0)
        +wallHelper(6,15,9,15)
        +wallHelper(7,12,7,14)
    ),
    'kimchi':[(15,11)]
}

eqDict = {
'equals':[(11,11),(10,6),
      (17,6),(16,11),
      (22,1),(13,2),
      (1,0),(1,2)],
    }

effectDict = {
    'open':[(12,11)],
    'shut':[(17,11)],
    'win':[(15,2)],
    'you':[(2,0)],
    'stop':[(2,2),(18,6)],
    'defeat':[(23,1)],
    'push':[(11,6)],
              }

subjDict = {
    'robotword':[(9,6)],
    'kimchiword':[(0,0)],
    'doorword':[(0,2)],
    'keyword':[(10,11),(21,1)],
    'wallword':[(16,6)]
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
print('level 12 load complete, result: ', levelDict, '\n\n')
level = level(12,levelDict,
              #level size
              (28,16), 
              #background colors
              rgb(45,59,123), rgb(16,21,40),
              #top margin
              10, 
              #bgm
              'sounds/music/float.ogg',
              #levelname
              'BURLGARY') 
