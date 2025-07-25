import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view')
from view.drawinfo import *

#these functions "load" data from the level dictionaries into the actual movement dictionary.
#names are just numbers. objects are not fixed to a certain state. 
#O1, O2, O3, etc. are objects;
#S1, S2, S3, etc. are subjects;
#I1, I2, I3, etc. are the 'is' statement equation operators;
#E1, E2, E3, etc. are effects;
#A1, A2, A3, etc. are adjectives.

def loadObjects(objDict):
    namecount = 0
    objectDictReturn = {}
    for objectName, positions in objDict.items():
        if isinstance(positions, tuple):
            objectDictReturn[obj(f'O{namecount}', objectName)] = positions
            namecount += 1
        elif isinstance(positions, list):
            for lIdx in range(len(positions)):
                objectDictReturn[obj(f'O{namecount}', objectName)] = positions[lIdx]
                namecount += 1 
    return objectDictReturn

def loadSubjs(subjDict):
    namecount = 0
    subjectDictReturn = {}
    for subjName, positions in subjDict.items():
        if isinstance(positions, tuple):
            subjectDictReturn[subj(f'S{namecount}', subjName, subjName[:-4])] = positions 
            namecount += 1
            #subject attributes are strictly the object names affixed with 'word.'
            #we get rid of the 'word' to get the object attribute with [:-4]
        elif isinstance(positions, list):
            for lIdx in range(len(positions)):
                subjectDictReturn[subj(f'S{namecount}', subjName,subjName[:-4])] = positions[lIdx]
                namecount += 1
    return subjectDictReturn

def loadEqs(eqDict):
    namecount = 0
    eqDictReturn = {}
    for eqName, positions in eqDict.items():
        if isinstance(positions, tuple):
            eqDictReturn[eq(f'I{namecount}', eqName)] = positions
            namecount += 1
        elif isinstance(positions, list):
            for lIdx in range(len(positions)):
                eqDictReturn[eq(f'I{namecount}', eqName)] = positions[lIdx]
                namecount += 1
    return eqDictReturn

def loadEffects(effectDict):
    namecount = 0
    effectDictReturn = {}
    for effectName, positions in effectDict.items():
        if isinstance(positions, tuple):
            effectDictReturn[effect(f'P{namecount}', effectName)] = positions
            namecount += 1
        elif isinstance(positions, list):
            for lIdx in range(len(positions)):
                effectDictReturn[effect(f'P{namecount}', effectName)] = positions[lIdx]
                namecount += 1
    return effectDictReturn

def loadAdjs(adjDict):
    namecount = 0
    adjDictReturn = {}
    for adjName, positions in adjDict.items():
        if isinstance(positions, tuple):
            adjDictReturn[adj(f'A{namecount}', adjName)] = positions
            namecount += 1
        elif isinstance(positions, list):
            for lIdx in range(len(positions)):
                adjDictReturn[adj(f'A{namecount}', adjName)] = positions[lIdx]
                namecount += 1
    return adjDictReturn

def loadPositions(levelDict):
    for item in levelDict:
        item.pos = levelDict[item]

#enumerate movements for efficiency
moveDict = {'right': (1,0), 'left':(-1,0), 'up':(0,-1),'down':(0,1)}

#(graphics) drawInfo dictionaries--------------------------------------
#read drawinfo.py for actual sprite / color / etc. 
objDrawDict = {'baba': babaDraw, 
            'rock': rockDraw, 
            'wall': wallDraw, 
            'flag': flagDraw,
            'equals': equalsDraw, 
            'has': hasDraw, 
            'you': youDraw, 
            'push': pushDraw,
            'stop': stopDraw, 
            'win': winDraw}

wordDrawDict = {'wallword': wallWordDraw, 
                'rockword': rockWordDraw, 
                'babaword': babaWordDraw, 
                'flagword': flagWordDraw, 
                'you': youDraw,
                'push': pushDraw,
                'stop': stopDraw,
                'win': winDraw,
                'equals': equalsDraw,
                'has': hasDraw
                }

#start actual class definitions--------------------------------------
#these labels are mine. I swear. this section isn't cursored. 
class obj:
    def __init__(self, name, attribute):
        #object base information (determines what object e.g. baba, keke, kimchi the object instance is)
        self.name = name #DO NOT MISTAKE FOR ATTRIBUTE! The name is for obj instance modification. 
        self.attribute = attribute #THIS is the name of the actual object (baba, rock, wall, flag, etc.)
        self.drawInfo = objDrawDict[self.attribute]
        self.initialState = self.attribute #initial state, for a full reset of the level
        
        #movement info
        self.pos = None
        self.posHist = []
        self.effectsList = []
        
        #drawing info
        self.direction = 'right'
        self.type = 'obj'
        
    def setAttribute(self, attribute):
        self.attribute = attribute 
        self.drawInfo = objDrawDict[attribute]
        
    #equals and hashing function for storage in level dictionary
    def __eq__(self,other):
        if isinstance(other, obj):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
        
    def __hash__(self):
        return hash(f'{self.name}, {self.attribute}')
    
    def __repr__(self):
        return f'{self.name}'

    #prelim implementation of the is you feature
    def addEffect(self,effect):
        self.effectsList += [effect]
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)

    def undoMove(self):
        oldPos, oldDirection = self.posHist.pop()
        self.pos = oldPos
        self.direction = oldDirection
        
    
    def resetPos(self):
        if self.posHist:
            if isinstance(self.posHist[0][1],str): #means direction data was stored.
                #need to unpack differently
                self.pos = self.posHist[0][0]
                self.direction = self.posHist[0][1]
                self.posHist = []
            else:
                self.pos = self.posHist[0]
                self.direction = 'right'
                self.posHist = []

#words-------------------------------------------------  
class subj:
    def __init__(self, name, attribute, obj):
        #word base information (determines what word it is)
        self.name = name
        self.attribute = attribute
        self.initialState = self.attribute
        
        #draw info
        self.drawInfo = wordDrawDict[attribute]
        self.direction = 'right'
        self.powered = False
        
        #rulemaking info
        self.obj = obj
        
        #movement info
        self.pos = None
        self.posHist = []
        self.effectsList = {'push'}
        
        #type info
        self.type = 'subj'
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)

    def undoMove(self):
        oldPos, oldDirection = self.posHist.pop()
        self.pos = oldPos
        self.direction = oldDirection
    
    def resetPos(self):
        if self.posHist:
            if isinstance(self.posHist[0][1],str): #means direction data was stored.
                #need to unpack differently
                self.pos = self.posHist[0][0]
                self.direction = self.posHist[0][1]
                self.posHist = []
            else:
                self.pos = self.posHist[0]
                self.direction = 'right'
                self.posHist = []
    
    def __eq__(self,other):
        if isinstance(other, subj):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
        
    def __hash__(self):
        return hash(f'{self.name}, {self.attribute}')
    
    def __repr__(self):
        return f'{self.name}'

class eq: #includes 'IS' and 'HAS'
    def __init__(self, name, attribute):
        #word base information (determines what word it is)
        self.name = name
        self.attribute = attribute
        self.initialState = self.attribute
        
        #rulemaking info
        self.subj= None
        self.desc = None
        self.effectsList = {'push'}
        
        #movement info
        self.pos = None
        self.posHist = []
        
        #drawing info
        self.powered = False
        self.direction = 'right'
        self.drawInfo = wordDrawDict[attribute]
        
        #comparison info
        self.type = 'eq'
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)

    def undoMove(self):
        oldPos, oldDirection = self.posHist.pop()
        self.pos = oldPos
        self.direction = oldDirection
    
    def resetPos(self):
        if self.posHist:
            if isinstance(self.posHist[0][1],str): #means direction data was stored.
                #need to unpack differently
                self.pos = self.posHist[0][0]
                self.direction = self.posHist[0][1]
                self.posHist = []
            else:
                self.pos = self.posHist[0]
                self.direction = 'right'
                self.posHist = []
        
    def makeSubject(self, other):
        self.subj = other
        
    def makeDescribe(self, other):
        if isinstance(other, effect):
            self.desc = other.desc
        
    def makeRule(self):
        if self.subj != None and self.desc != None:
            self.subj.addEffect(self.desc)
        
    def __eq__(self,other):
        if isinstance(other, eq):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
        
    def __hash__(self):
        return hash(f'{self.name}, {self.attribute}')
    
    def __repr__(self):
        return f'{self.name}'
        
class effect: #includes (YOU, STOP, MELT, SINK, WIN)
    def __init__(self, name, attribute):
        #effect base information
        self.name = name
        self.attribute = attribute
        self.initialState = self.attribute
        
        #movement info
        self.pos = None
        self.posHist = []
        self.effectsList = {'push'}
        
        self.drawInfo = wordDrawDict[attribute]
        self.powered = False
        self.color = self.drawInfo.color ##legacy, remove when sprites implemented
        self.direction = 'right'
        
        #type info
        self.type = 'effect'
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)
        
    def undoMove(self):
        oldPos, oldDirection = self.posHist.pop()
        self.pos = oldPos
        self.direction = oldDirection
    
    def resetPos(self):
        if self.posHist:
            if isinstance(self.posHist[0][1],str): #means direction data was stored.
                #need to unpack differently
                self.pos = self.posHist[0][0]
                self.direction = self.posHist[0][1]
                self.posHist = []
            else:
                self.pos = self.posHist[0]
                self.direction = 'right'
                self.posHist = []
        
    def __eq__(self,other):
        if isinstance(other, effect):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
        
    def __hash__(self):
        return hash(f'{self.name}, {self.attribute}')
    
    def __repr__(self):
        return f'{self.attribute}'


class adj: #includes (NOT, AND)
    def __init__(self, name, drawInfo):
        #adj base information
        self.name = name
        
        #draw info
        self.drawInfo = drawInfo
        
        #movement info
        self.pos = None
        self.posHist = []
        
        #type info
        self.type = 'adj'
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)

    def undoMove(self):
        oldPos, oldDirection = self.posHist.pop()
        self.pos = oldPos
        self.direction = oldDirection
    
    def resetPos(self):
        if self.posHist:
            if isinstance(self.posHist[0][1],str): #means direction data was stored.
                #need to unpack differently
                self.pos = self.posHist[0][0]
                self.direction = self.posHist[0][1]
                self.posHist = []
            else:
                self.pos = self.posHist[0]
                self.direction = 'right'
                self.posHist = []
        
    def __eq__(self,other):
        if isinstance(other, adj):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
    
    def __hash__(self):
        return hash(f'{self.name}, {self.attribute}')
    
    def __repr__(self):
        return f'{self.name}'

#map and level---------------
class level: 
    def __init__(self, num, dict, size):
        self.num = num #number for loading
        self.dict = dict #storage of object positions
        self.wd = {} #wd stands for 'word dictionary' (idk too lazy)
        self.rules = [] 
        self.size = size
        self.moveHistory = [] #this stores tuples with either (obj.name, move) move data
        #or object change data: (obj.name, oldtype, newtype)
