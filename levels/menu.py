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
objDict = {'menu': [(2,1)],
           'kimchi': [(4,6)]}

subjDict = {'start': [(5,6)],
            'continue': [(5,8)],
            'settings': [(5,10)],
            'exit': [(5,12)]}

#now we load the level into the levelDict. 
#load function is in objects.py
levelDict.update(loadObjects(objDict)) 
levelDict.update(loadSubjs(subjDict))
loadPositions(levelDict)
print('menu load complete, result: ', levelDict)
level = level(0,levelDict,(17,13),'black', 'black', 10,'sounds/music/menu.ogg', 'MENU',True, False) #store the size of the level here.
#i spent ~40 lines in total checking for the stupid 'str' entry in the level dictionary
#before i figured i could just make a new class attribute.

#bruh fts

#(2, 1): menu icon

#(5 ,6): play button, 8 wide