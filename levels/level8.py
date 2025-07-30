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
    wallHelper(5,2,18,2)
    +wallHelper(5,11,18,11)
    +wallHelper(18,3,18,10)
    +wallHelper(5,3,5,10)
), 
'grass':(
    wallHelper(12,7,12,9)
    +[(10,3),(6,5),(6,8),(7,9),
      (10,10),(13,5),(14,6),(15,7),
      (15,9),(13,10),(16,6),(17,7)]
),
'keke':[(9,7)],
'flag':[(16,4)],
}

eqDict = {
    'equals':[(8,4),(23,7)]
    }

effectDict = {
    'you':[(9,4)],
    'win':[(16,8)],
    'stop':[(23,8)],
              }

subjDict = {
    'kekeword':[(7,4)],
    'flagword':[(14,8)],
    'grassword':[(23,6)]
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
print('level 8 load complete, result: ', levelDict, '\n\n')
level = level(8,levelDict,
              #level size
              (24,14), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'GRASS YARD') 
