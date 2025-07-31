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
objDict = {'kimchi':[(11,13)],
           'key':[(11,8)],
    'wall':(wallHelper(9,2,16,2)
                   +wallHelper(9,3,9,6)
                   +wallHelper(5,6,8,6)
                   +wallHelper(5,7,5,10)
                   +wallHelper(6,10,15,10)
                   +wallHelper(9,11,9,16)
                   +wallHelper(10,16,15,16)
                   +wallHelper(16,3,16,4)
                   +wallHelper(16,6,16,16)
                   ),
    'door':[(16,5)]}

eqDict = {
    'equals':[(6,13),(13,13),(24,3),(24,4),(23,5)]
}

effectDict = {
    'you':[(6,14)],
    'win':[(9,8)],
    'open':[(25,4)],
    'shut':[(25,3)],
    'push':[(23,6)]
}

subjDict = {'doorword':[(23,3)],
            'wallword':[(13,12)],
            'kimchiword':[(23,4)],
            'keyword':[(6,12)]}

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