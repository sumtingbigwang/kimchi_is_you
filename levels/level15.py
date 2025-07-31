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
           'baba' : (4,6),
           'leaf' : [(8,5),(8,6),(8,7)],
           'tree' : [(i,4) for i in range(3,14)] + [(i,8) for i in range(3,14)]}

eqDict = {'equals': [(4,1), (4,10),(12,1),(12,10),(1,0)]}

effectDict = {'push': [(13,1)],
              'stop': [(13,10)],
              'win': [(5,10)],
              'you': [(5,1)],
              'float':[(2,0)]}

subjDict = {'treeword': [(11,10)],
               'leafword': [(11,1)],
               'babaword': [(3,1),(0,0)],
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
print('level 15 load complete, result: ', levelDict, '\n\n')
level = level(15,levelDict,
              #level size
              (17,13), 
              #background colors
              rgb(82,64,40), rgb(55,45,37),
              #top margin
              10, 
              #bgm
              'sounds/music/forest.ogg',
              #levelname
              'FLOAT') 
