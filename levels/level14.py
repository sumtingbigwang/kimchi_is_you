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
'fence':(
    wallHelper(6,3,17,3)
    +wallHelper(6,4,6,14)
    +wallHelper(17,4,17,14)
    +wallHelper(7,14,16,14)
),
'baba':[(9,8)],
'brick':(
    wallHelper(14,6,16,6)
    +wallHelper(13,7,15,7)
    +wallHelper(13,8,15,8)
    +wallHelper(14,9,15,9)
    +wallHelper(7,11,8,11)
),
'tile':[(10,5),(12,5),(14,5)],
'tree':[(1,16),(21,3),(3,6)]
}

eqDict = {
'equals':[(13,8),(1,0),(1,1),(20,8)],
'not':[(2,0),(14,5)]
    }

effectDict = {
    'you':[(3,0),(14,8)],
    'stop':[(2,1),(10,5)],
    'win':[(20,9)]
              }

subjDict = {
'babaword':[(12,8)],
'fenceword':[(0,0),(0,1),(12,5)]
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
print('level 14 load complete, result: ', levelDict, '\n\n')
level = level(14,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(82,64,40), rgb(55,45,37),
              #top margin
              10, 
              #bgm
              'sounds/music/forest.ogg',
              #levelname
              'NOT THERE') 
