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
'skull':(
    wallHelper(12,0,12,7)
    +wallHelper(13,7,23,7)
),
'wall':(
    [(15,4),(15,2),(11,1)]
    +wallHelper(6,4,6,8)
    +wallHelper(7,8,9,8)
    +wallHelper(10,7,10,11)
    +wallHelper(11,11,15,11)
    +wallHelper(15,8,15,10)
    +wallHelper(13,6,15,6)
    +wallHelper(15,5,19,5)
    +wallHelper(19,1,19,4)
    +wallHelper(13,1,18,1)
    +wallHelper(10,1,10,5)
    +wallHelper(7,4,9,4)
),
'rock':(wallHelper(4,0,4,6)
        +wallHelper(0,6,3,6)
),
'baba':[(8,6)],
'flag':[(17,3)]
}

eqDict = {
'equals':[(1,0),(1,2),(1,4),(8,11),(13,9)]
    }

effectDict = {
'you':[(8,12)],
'win':[(2,4)],
'stop':[(14,9),(2,0)],
'defeat':[(2,2)]
              }

subjDict = {
'babaword':[(8,10)],
'rockword':[(0,0)],
'skullword':[(0,2)],
'flagword':[(0,4)],
'wallword':[(12,9)],
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
print('level 7 load complete, result: ', levelDict, '\n\n')
level = level(7,levelDict,
              #level size
              (24,14), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'OFF LIMITS') 
