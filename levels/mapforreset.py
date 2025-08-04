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
#MAP: PUT THE LEVEL POSITIONS FROM BOTTOM OF SCREEN TO TOP OF SCREEN.
objDict = {'cursor':[(7,13)],
           'tile':[#tutorial levels
                   (7,13),(8,13),(9,13),
                   (7,12),(8,12),(9,12),
                   (7,11),(8,11),(9,11),
                   
                   #the lake
                   (12,12),(13,12),(14,12),
                   
                   #forest of fall
                   (19,12),(20,12),(21,12),
                   
                   #the factory
                   (23,9), (24,9),
                   
                   #meta
                   (15,2),(14,2),(13,2),(12,2),(2,5)
                   ],
        'line':(
                wallHelper(15,12,18,12)
                +wallHelper(22,5,22,8)
                +wallHelper(15,5,21,5)
                +[(10,12),(11,12),(21,11),(21,10),(21,9),(22,9),(15,3),(15,4)])
        }
subjDict = {'kimchiword': [(29,15)],
            'flagword': [(29,17)],
            'tileword': [(0,0)]}
eqDict = {'equals': [(30,15),(30,17),(1,0)]}

effectDict = {'you': [(31,15)],
              'win': [(31,17)],
              'stop':[(2,0)]}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
loadPositions(levelDict)
print('map load complete, result: ', levelDict)
level = level(-2,levelDict,(32,18),None, 
              None, 20,'sounds/music/map.ogg', 'MAP',False, True) #store the size of the level here.
