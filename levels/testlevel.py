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
    'kimchi':[(6,4)],
    'rock':[(6,9)],
    }

eqDict = {
    'equals':[(6,2),(6,11)],
}

effectDict = {
    'you':[(7,2)],
    'push':[(7,11)],
}

subjDict = {
    'kimchiword':[(5,2)],
    'rockword':[(5,11)],
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
print('testlevel load complete, result: ', levelDict)
level = level(69,levelDict,
              #level size
              (13,13), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/ending.ogg',
              #levelname
              'METAMETA(HOSTILE ENVIRONMENT)')#store the size of the level here.
#i spent ~40 lines in total checking for the stupid 'str' entry in the level dictionary
#before i figured i could just make a new class attribute.

#bruh fts