import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view')
from view.drawinfo import *
import copy 

#NOT:
# if NOT object is effect: 
# for entry in levelDict:
#     if entry.attribute != object.attribute:
#         if entry.effectsList += effect.attribute

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
            if objectName == 'cursor':
                objectDictReturn[obj(f'O{namecount}', objectName, ('you','float'))] = positions
            else:
                objectDictReturn[obj(f'O{namecount}', objectName)] = positions
            namecount += 1
        elif isinstance(positions, list):
            for position in positions:
                objectDictReturn[obj(f'O{namecount}', objectName)] = position
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
objDrawDict = {
            #sprites--------------------------------
            #player sprites--------------------------------
            'baba': babaDraw, 
            'kimchi': kimchiDraw,
            'keke': kekeDraw,
            'jiji': jijiDraw,
            'kosbie': kosbieDraw,
            'it': itDraw,
            'me': meDraw,

            #semi-player sprites--------------------------------
            'robot': robotDraw,
            'frog': frogDraw,
            'eye': eyeDraw,
            'belt': beltDraw,
            'skull': skullDraw,
            'ghost': ghostDraw,
            'bird': birdDraw,
            'rocket': rocketDraw,
            
            #object sprites--------------------------------
            'rock': rockDraw, 
            'flag': flagDraw,
            'tile': tileDraw,
            'bolt': boltDraw,
            'arrow': arrowDraw,
            'jelly': jellyDraw,
            'algae': algaeDraw,
            'door': doorDraw,
            'key': keyDraw,
            'tree': treeDraw,
            'leaf': leafDraw,
            
            #wall sprites
            'wall': wallDraw, 
            'water': waterDraw,
            'lava': lavaDraw,
            'ice': iceDraw,
            'hedge': hedgeDraw,
            'grass': grassDraw,
            'fence': fenceDraw,
            'brick': brickDraw,
            'line': lineDraw,
            'pipe': pipeDraw,
            
            #words--------------------------------
            'equals': equalsDraw, 
            'not': notDraw,
            
            #effects--------------------------------
            'has': hasDraw, 
            'you': youDraw, 
            'push': pushDraw,
            'stop': stopDraw, 
            'win': winDraw, 
            
            
            #menu-related items--------------------------------
            'menu': menuDraw,
            'cursor': cursorDraw}

wordDrawDict = {
                #object words--------------------------------
                'wallword': wallWordDraw, 
                'rockword': rockWordDraw, 
                'babaword': babaWordDraw, 
                'flagword': flagWordDraw, 
                'tileword': tileWordDraw,
                'kimchiword': kimchiWordDraw,
                'kosbieword': kosbieWordDraw,
                'kekeword': kekeWordDraw,
                'jijiword': jijiWordDraw,
                'meword': meWordDraw,
                'robotword': robotWordDraw,
                'itword': itWordDraw,
                'frogword': frogWordDraw,
                'eyeword': eyeWordDraw,
                'waterword': waterWordDraw,
                'lavaword': lavaWordDraw,
                'iceword': iceWordDraw,
                'hedgeword': hedgeWordDraw,
                'grassword': grassWordDraw,
                'fenceword': fenceWordDraw,
                'brickword': brickWordDraw,
                'lineword': lineWordDraw,
                'allword': allDraw,
                'skullword': skullWordDraw,
                'ghostword': ghostWordDraw,
                'birdword': birdWordDraw,
                'boltword': boltWordDraw,
                'arrowword': arrowWordDraw,
                'rocketword': rocketWordDraw,
                'jellyword': jellyWordDraw,
                'algaeword': algaeWordDraw,
                'doorword': doorWordDraw,
                'keyword': keyWordDraw,
                'treeword': treeWordDraw,
                'leafword': leafWordDraw,
                'pipeword': pipeWordDraw,
                'textword': textWordDraw,
                
                #effect words--------------------------------
                'you': youDraw,
                'push': pushDraw,
                'stop': stopDraw,
                'win': winDraw,
                'sink': sinkDraw,
                'defeat': defeatDraw,
                'hot': hotDraw,
                'melt': meltDraw,
                'open': openDraw,
                'shut': shutDraw,
                'float': floatDraw,
                'weak': weakDraw,
                'empty': emptyDraw,
                'text': textWordDraw,
                'level': levelWordDraw,
                'done': doneDraw,
                'move': moveWordDraw,
                'more': moreWordDraw,
                'shift': shiftWordDraw,
                'open': openWordDraw,
                'shut': shutWordDraw,
                'not': notDraw,
                
                #equal words--------------------------------
                'equals': equalsDraw,
                'has': hasDraw,
                'and': andDraw,
                'on': onDraw,
                'lonely': lonelyDraw,
                'eat': eatDraw,
                
                #button words--------------------------------
                'start': startDraw,
                'continue': continueDraw,
                'settings': settingsDraw,
                'exit': exitDraw
                }

#start actual class definitions--------------------------------------
#these labels are mine. I swear. this section isn't cursored. 
class obj:
    def __init__(self, name, attribute, initEffect = None, initDirection = 'down'):
        #object base information (determines what object e.g. baba, keke, kimchi the object instance is)
        self.name = name #DO NOT MISTAKE FOR ATTRIBUTE! The name is for obj instance modification. 
        self.attribute = attribute #THIS is the name of the actual object (baba, rock, wall, flag, etc.)
        self.drawInfo = objDrawDict[self.attribute]
        self.initialState = self.attribute #initial state, for a full reset of the level
        self.stateCount = 0
        self.powered = False
        
        #movement info
        self.pos = None
        self.posHist = []
        self.effectsList = [initEffect] if initEffect else []  #if initEffect is not None, add it to the effectsList
        self.preSink = None
        
        #drawing info
        self.direction = initDirection
        self.type = 'obj'
        
    def setAttribute(self, attribute):
        self.attribute = attribute 
        self.drawInfo = objDrawDict[attribute]
        
    #equals and hashing function for storage in level dictionary
    def __eq__(self,other):
        if isinstance(other, obj):
            return (self.name == other.name)
        
    def __hash__(self):
        return hash(f'{self.name}')
    
    def __repr__(self):
        return f'{self.name}'

    #prelim implementation of the is you feature
    def addEffect(self,effect):
        self.effectsList += [effect]
    
    def changeDir(self, direction): #for running into walls
        self.direction = direction
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)
        self.stateCount = (self.stateCount + 1) % 4 #update state count

    def undoMove(self):
        if self.posHist:
            oldPos, oldDirection = self.posHist.pop()
            self.pos = oldPos
            self.direction = oldDirection
            self.stateCount = (self.stateCount - 1) % 4 #update state count
    
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
            self.stateCount = 0
        self.attribute = self.initialState
        self.drawInfo = objDrawDict[self.attribute]

#words-------------------------------------------------  
class subj:
    def __init__(self, name, attribute, obj, powered=False):
        #word base information (determines what word it is)
        self.name = name
        self.attribute = attribute
        self.initialState = self.attribute
        
        #draw info
        self.drawInfo = wordDrawDict[attribute]
        self.direction = 'right'
        self.powered = powered
        
        #rulemaking info
        self.obj = obj
        self.rootOperator = None
        self.rootSubj = None
        self.rootEffect = None
        
        #movement info
        self.pos = None
        self.posHist = []
        self.effectsList = ['push'] 
        self.preSink = None
        
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

    def changeDir(self, direction): #for running into walls
        self.direction = direction
    
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
            return (self.name == other.name)
        
    def __hash__(self):
        return hash(f'{self.name}')
    
    def __repr__(self):
        return f'{self.name}'

class eq: #includes 'IS' and 'HAS'
    def __init__(self, name, attribute):
        #word base information (determines what word it is)
        self.name = name
        self.attribute = attribute
        self.initialState = self.attribute
        
        #rulemaking info
        self.effectsList = ['push']
        self.rootSubj = None
        self.rootEffect = None
        
        #movement info
        self.pos = None
        self.posHist = []
        self.preSink = None
        
        #drawing info
        self.powered = False
        self.direction = 'right'
        self.drawInfo = wordDrawDict[attribute]
        
        #comparison info
        self.type = 'eq'
        
    
    def changeDir(self, direction): #for running into walls
        self.direction = direction
    
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
        if isinstance(other, eq):
            return (self.name == other.name 
                    and self.attribute == other.attribute)
        
    def __hash__(self):
        return hash(f'{self.name}')
    
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
        self.effectsList = ['push']
        self.preSink = None
        self.drawInfo = wordDrawDict[attribute]
        self.powered = False
        self.color = self.drawInfo.color ##legacy, remove when sprites implemented
        self.direction = 'right'
        
        #type info
        self.type = 'effect'
        
        #rule making info
        self.rootSubj = None
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)
        
    def changeDir(self, direction): #for running into walls
        self.direction = direction
        
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
            return (self.name == other.name)
        
    def __hash__(self):
        return hash(f'{self.name}')
    
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
        self.effectsList = ['push']
        self.preSink = None
        
        #type info
        self.type = 'adj'
    
    def MoveObject(self, direction):
        self.posHist.append((self.pos,self.direction))
        x, y = self.pos
        dx, dy = moveDict[direction]
        self.direction = direction
        self.pos = (x + dx, y + dy)
    
    def changeDir(self, direction): #for running into walls
        self.direction = direction

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
            return (self.name == other.name)
    
    def __hash__(self):
        return hash(f'{self.name}')
    
    def __repr__(self):
        return f'{self.name}'

#map and level---------------
class level: 
    def __init__(self, num, dict, size, background, cellColor, margin=10, 
                 bgm=None, levelName='', inMenu=False, inMap=False):
        self.num = num #number for loading
        self.dict = dict #storage of object positions
        self.wd = {} #wd stands for 'word dictionary' (idk too lazy)
        self.rules = [] 
        self.size = size
        self.background = background
        self.cellColor = cellColor
        self.margin = 10
        self.bgm = bgm
        self.moveHistory = [] #this stores tuples with either (obj.name, move) move data
        #or object change data: (obj.name, oldtype, newtype)
        self.inMenu = inMenu
        self.inMap = inMap
        self.levelName = levelName