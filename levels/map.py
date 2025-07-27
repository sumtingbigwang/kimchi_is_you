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
#MAP: PUT THE LEVEL POSITIONS FROM BOTTOM OF SCREEN TO TOP OF SCREEN.
objDict = {'cursor':[(7,13)],
           'tile':[(7,13),(8,13),(9,13),
                   (7,12),(8,12),(9,12),
                   (7,11),(8,11),(9,11)]}
subjDict = {'babaword': [(29,15)],
            'flagword': [(29,17)]}
eqDict = {'equals': [(30,15),(30,17)]}

effectDict = {'you': [(31,15)],
              'win': [(31,17)]}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
loadPositions(levelDict)
print('level load complete, result: ', levelDict)
level = level(-1,levelDict,(32,18),None, 
              None, 10,'sounds/music/map.ogg', False, True) #store the size of the level here.
