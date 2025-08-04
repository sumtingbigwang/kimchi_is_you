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
        [(19,13),(18,11),(6,6),(6,2),(8,7)]
        +wallHelper(4,6,4,16)
        +wallHelper(5,16,17,16)
        +wallHelper(15,12,15,15)
        +wallHelper(17,14,17,15)
        +wallHelper(18,14,19,14)
        +wallHelper(16,12,19,12)
        +wallHelper(15,1,15,10)
        +wallHelper(7,1,14,1)
        +wallHelper(7,2,7,6)
        +wallHelper(5,2,5,6)
        +wallHelper(8,6,10,6)
        +wallHelper(12,6,14,6)
        +wallHelper(12,7,12,8)
    ),
    'door':[(15,11)],
    'kimchi':[(8,11)],
    'key':[(6,11)]
}

eqDict = {
    'equals':[(6,4),(5,8),(10,7),
              (17,8),(18,7),(16,14),
              (17,13),(8,13),(13,13)]
}

effectDict = {
    'you':[(9,13)],
    'win':[(11,3)],
    'stop':[(5,9)],
    'defeat':[(18,13),(19,7)],
    'weak':[(11,8)],
    'hot':[(14,13)],
    'melt':[(17,9)]
}

subjDict = {
    'kimchiword':[(7,13)],
    'keyword':[(6,3),(6,5),(12,13)],
    'doorword':[(17,7)],
    'wallword':[(5,7),(16,13),(16,15)],
    'level':[(9,7)]
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
print('level 21 load complete, result: ', levelDict, '\n\n')
level = level(21,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'META(FRAGILE EXISTENCE)')