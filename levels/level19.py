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
    'hedge':(
        [(18,7),(14,14),(13,15),(19,13),(12,9)]
        +wallHelper(3,0,3,3)
        +wallHelper(0,1,2,1)
        +wallHelper(0,3,2,3)
        +wallHelper(15,3,16,3)
        +wallHelper(17,3,17,10)
        +wallHelper(14,9,16,9)
        +wallHelper(19,7,19,11)
        +wallHelper(12,11,18,11)
        +wallHelper(18,13,18,15)
        +wallHelper(14,13,17,13)
        +wallHelper(14,15,17,15)
        +wallHelper(20,11,20,13)
        +wallHelper(12,12,12,15)
        +wallHelper(6,14,11,14)
        +wallHelper(10,11,10,13)
        +wallHelper(7,12,9,12)
        +wallHelper(6,10,6,13)
        +wallHelper(5,7,5,10)
        +wallHelper(6,6,6,7)
        +wallHelper(11,5,11,7)
        +wallHelper(12,5,15,5)
    ),
    'baba':[(12,3)],
    'rock':[(13,7),(15,7)],
    'tree':[(16,4)],
    'flag':[(11,13)],
    'water':(
        wallHelper(7,6,7,11)
        +wallHelper(6,8,6,9)
        +wallHelper(8,6,8,8)
        +wallHelper(8,10,8,11)
        +wallHelper(9,6,9,7)
        +wallHelper(10,6,10,7)
        +[(9,11)]
    )
}

eqDict = {
    'equals':[(18,9),(14,12),(16,14),
              (13,13),(8,13),(1,0),
              (1,2),(11,10),(8,2),(17,12)],
    'not':[(18,12),(13,10),(6,2)],
          }

effectDict = {
    'you':[(14,10),(2,0)],
    'float':[(2,2)],
    'win':[(17,14)],
    'push':[(9,3),(19,12)],
    'stop':[(15,12)],
    'sink':[(9,13)],
}

subjDict = {
    'hedgeword':[(13,12),(13,14),(16,12)],
    'flagword':[(15,14)],
    'waterword':[(7,13)],
    'rockword':[(18,8),(18,10),(7,2)],
    'babaword':[(0,0),(10,10)],
    'textword':[(0,2)],
    'treeword':[(0,17)]
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
print('level 19 load complete, result: ', levelDict, '\n\n')
level = level(19,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(82,64,40), rgb(55,45,37),
              #top margin
              10, 
              #bgm
              'sounds/music/forest.ogg',
              #levelname
              'CATCH') 
