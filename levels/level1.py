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
objDict = {'flag' : (12, 6),
           'kimchi' : (4,6),
           'rock' : [(8,5),(8,6),(8,7)],
           'wall' : [(i,4) for i in range(3,14)] + [(i,8) for i in range(3,14)]}

eqDict = {'equals': [(4,1), (4,10),(12,1),(12,10)]}

effectDict = {'push': [(13,1)],
              'stop': [(13,10)],
              'win': [(5,10)],
              'you': [(5,1)]}

subjDict = {'wallword': [(11,10)],
               'rockword': [(11,1)],
               'kimchiword': [(3,1)],
               'flagword': [(3,10)]}

adjDict = {} #no adjectives in this level. 

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
levelDict.update(loadAdjs(adjDict))

loadPositions(levelDict)
print('level 1 load complete, result: ', levelDict, '\n\n')
level = level(1,levelDict,
              # level size
              (17,13), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #level name
              'STARTING OFF')
#i spent ~40 lines in total checking for the stupid 'str' entry in the level dictionary
#before i figured i could just make a new class attribute.

#bruh fts