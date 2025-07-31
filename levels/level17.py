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
        [(2,6),(3,7),(3,9),
         (11,14),(14,13),(11,4)]
        +wallHelper(0,7,1,7)
        +wallHelper(0,9,1,9)
        +wallHelper(6,13,9,13)
        +wallHelper(9,12,12,12)
        +wallHelper(11,9,11,11)
        +wallHelper(6,9,10,9)
        +wallHelper(6,10,6,12)
        +wallHelper(5,7,11,7)
        +wallHelper(2,5,11,5)
        +wallHelper(4,9,4,15)
        +wallHelper(5,15,14,15)
        +wallHelper(14,14,20,14)
        +wallHelper(20,3,20,13)
        +wallHelper(11,3,19,3)
    ),
    'skull':[(6,6),(6,8),(5,9)],
    'kosbie':[(11,6)],
    'me':[(15,11)],
    'bolt':[(17,11)],
    'pipe':(
        wallHelper(19,16,23,16)
        +wallHelper(0,1,23,1)
        +[(19,17),(8,0),(18,0)]
    )
}

eqDict = {
    'equals':[(21,8),(16,7),(4,7),(2,8),(9,4),(9,11)]
}

effectDict = {
    'push':[(17,7)],
    'win':[(11,13)],
    'you':[(2,9)],
    'defeat':[(10,4),(11,8)],
    'melt':[(21,9)],
    'stop':[(10,11)],
    'move':[(16,8)],
    'hot':[(4,8)]
}

subjDict = {
    'skullword':[(4,6)],
    'kosbieword':[(8,4)],
    'meword':[(2,7)],
    'wallword':[(8,11)],
    'boltword':[(15,7),(21,7)]
}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))

loadPositions(levelDict)
print('level 17 load complete, result: ', levelDict, '\n\n')
level = level(17,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(65,46,46), rgb(20,13,13),
              #top margin
              10, 
              #bgmgg
              'sounds/music/factory.ogg',
              #levelname
              'RESEARCH LAB') 
