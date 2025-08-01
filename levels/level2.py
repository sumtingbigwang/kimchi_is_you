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
objDict = {'kimchi':[(14,13)],
           'flag':[(11,8)],
    'wall':(wallHelper(9,2,16,2)
                   +wallHelper(9,3,9,6)
                   +wallHelper(5,6,8,6)
                   +wallHelper(5,7,5,10)
                   +wallHelper(6,10,15,10)
                   +wallHelper(9,11,9,16)
                   +wallHelper(10,16,15,16)
                   +wallHelper(16,3,16,16)
                   )}

eqDict = {
    'equals':[(6,13),(11,13)]
}

effectDict = {
    'you':[(6,14)],
    'stop':[(11,14)],
    'win':[(13,7)]
}

subjDict = {'wallword':[(11,12)],
            'kimchiword':[(6,12)],
            'flagword':[(7,8)]}

adjDict = {} #no adjectives in this level. 

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
levelDict.update(loadAdjs(adjDict))

loadPositions(levelDict)
print('level 2 load complete, result: ', levelDict, '\n\n')
level = level(2,levelDict,
              #level size
              (24,18), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'WHERE DO I GO?')