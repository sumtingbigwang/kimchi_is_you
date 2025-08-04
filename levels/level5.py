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
    'skull':(
        wallHelper(13,3,21,3)
        +wallHelper(21,4,21,11)
        +wallHelper(13,11,20,11)
        +wallHelper(13,4,13,10)
        +wallHelper(3,9,3,13)
        +wallHelper(9,9,9,13)
        +wallHelper(5,7,5,9)
        +wallHelper(7,7,7,9)
        +[(4,9),(8,9)]),
    'kimchi':[(6,12)],
    'rock': (wallHelper(6,8,6,10)),
    'flag':[(18,9)]
}

eqDict = {
    'equals':[(15,6),(1,0),(1,1),(3,5)]
    }

effectDict = {
    'push':[(4,5)],
    'win':[(2,0)],
    'you':[(2,1)],
    'defeat':[(15,7)]
              }

subjDict = {
    'kimchiword':[(0,1)],
    'skullword':[(15,5)],
    'rockword':[(2,5)],
    'flagword':[(0,0)],   
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
print('level 5 load complete, result: ', levelDict, '\n\n')
level = level(5,levelDict,
              #level size
              (24,14), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'STILL OUT OF REACH') 
