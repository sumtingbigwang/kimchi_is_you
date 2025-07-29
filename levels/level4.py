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
objDict = {'wall':(wallHelper(0,3,2,2)
                  +wallHelper(2,0,2,3)
                  +wallHelper(7,1,14,1)
                  +wallHelper(14,2,14,6)
                  +wallHelper(7,2,7,7)
                  +wallHelper(4,7,6,7)
                  +wallHelper(4,8,4,14)
                  +wallHelper(5,14,17,14)
                  +wallHelper(17,7,17,13)
                  +wallHelper(11,7,16,7)
                  +wallHelper(11,8,11,10)
                  +wallHelper(11,12,11,13)
                  +wallHelper(0,3,1,3)
                  +[(9,11)]),
           'water':(wallHelper(8,7,10,7)
                    +wallHelper(5,11,7,11)
                    +wallHelper(5,12,7,12)
                    +wallHelper(6,13,7,13)),
            'kimchi':[(9,3)],
            'rock':[(12,3),(12,5)],
            'flag':[(5,13)]
           }

eqDict = {'equals':[(0,1),(1,1),(6,5),(14,9),(14,12)]}

effectDict = {'push':[(15,9)],
              'win':[(15,12)],
              'sink':[(6,6)],
              'you':[(0,2)],
              'stop':[(1,2)]}

subjDict = {'kimchiword':[(0,0)],
            'wallword':[(1,0)],
            'rockword':[(13,9)],
            'flagword':[(13,12)],
            'waterword':[(6,4)]}

adjDict = {} #no adjectives in this level. 

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
levelDict.update(loadEqs(eqDict))
levelDict.update(loadEffects(effectDict))
levelDict.update(loadAdjs(adjDict))

loadPositions(levelDict)
print('level 4 load complete, result: ', levelDict)
level = level(4,levelDict,
              #level size
              (22,16), 
              #background colors
              rgb(21,24,31), 'black',
              #top margin
              10, 
              #bgm
              'sounds/music/baba.ogg',
              #levelname
              'OUT OF REACH') 
