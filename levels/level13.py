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
'hedge':(
    wallHelper(8,0,8,3)
    +wallHelper(9,3,20,3)
    +wallHelper(20,4,20,16)
    +wallHelper(12,16,19,16)
    +wallHelper(12,11,12,13)
    +wallHelper(10,10,16,10)
    +wallHelper(0,9,10,9)
    +wallHelper(12,15,12,17)
    +[(16,9),(10,14)]
),
'baba':[(6,7)],
'tree':(wallHelper(9,5,9,8)),
'rock':[(18,7),(12,14)],
'flag':[(7,15)],
'leaf':(wallHelper(17,9,19,9)
    +wallHelper(17,10,19,10)
)
}

eqDict = {
'equals':[(10,2),(7,13),(14,11),
          (18,4),(13,6),(12,7)]
    }

effectDict = {
'stop':[(11,2)],
'defeat':[(19,4)],
'weak':[(12,8)],
'you':[(14,6)],
'push':[(15,11)],
'win':[(9,12)]
              }

subjDict = {
'hedgeword':[(9,2)],
'babaword':[(12,6)],
'leafword':[(17,4)],
'rockword':[(13,11)],
'flagword':[(6,13)]
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
print('level 13 load complete, result: ', levelDict, '\n\n')
level = level(13,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(82,64,40), rgb(55,45,37),
              #top margin
              10, 
              #bgm
              'sounds/music/forest.ogg',
              #levelname
              'FRAGILITY') 
