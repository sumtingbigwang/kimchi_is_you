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
 'algae':(
    wallHelper(11,0,11,17)
    +wallHelper(12,0,12,17)
 ),
 'wall':(
     [(17,0),(19,5),(18,7),(22,7),(15,16),(22,14),(23,14),(22,15)]
     +wallHelper(21,0,21,7)
     +wallHelper(17,1,20,1)
     +wallHelper(22,8,23,8)
     +wallHelper(21,15,21,17)
 ),
 'kimchi':[(3,3),(2,14),(6,11)],
 'keke':[(5,7)],
 'flag':[(18,12)]
}

eqDict = {
    'equals':[(5,5),(8,8),(19,0),(20,3),(19,6),(18,14)],
    'and':[(20,5)]
    }

effectDict = {
    'you':[(8,9)],
    'win':[(19,14)],
    'move':[(6,5)],
    'push':[(5,9)],
    'stop':[(20,0)],
    'defeat':[(20,6)]
              }

subjDict = {
    'kimchiword':[(4,5),(20,2),(20,4)],
    'flagword':[(17,14)],
    'kekeword':[(8,7)],
    'wallword':[(18,0)],
    'algaeword':[(18,6)]
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
print('level 20 load complete, result: ', levelDict, '\n\n')
level = level(20,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(45,59,123), rgb(16,21,40),
              #top margin
              10, 
              #bgm
              'sounds/music/ruin.ogg',
              #levelname
              'FURTHER FIELDS') 
