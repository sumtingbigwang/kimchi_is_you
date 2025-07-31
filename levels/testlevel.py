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
    'kimchi':[(16,5)],
    'rock':[(16,10)],
    }

eqDict = {
    'equals':[(16,3),(16,12)],
}

effectDict = {
    'you':[(17,3)],
    'push':[(17,12)],
}

subjDict = {
    'kimchiword':[(15,3)],
    'rockword':[(15,12)],
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
              (33,18), 
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