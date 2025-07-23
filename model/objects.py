#objects-----------------------------------------------     
class obj:
    def __init__(self, name, dir, color, labelcolor): 
        #remove color and labelcolor later
        #replace with sprite link instead
        self.dir = dir
        self.name = name
        self.color = color
        self.labelcolor = labelcolor
        self.eff = []
        self.type = 'obj'
        
    #equals and hashing function for storage in level dictionary
    def __eq__(self,other):
        if isinstance(other, obj):
            return self.name == other.name and self.eff == other.eff
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f'{self.name}'

    #prelim implementation of the is you feature
    def addEffect(self,effect):
        self.eff += [effect]
        

#words-------------------------------------------------
class subj: #includes(BABA, KEKE, FLAG, ROCK, WALL)
    def __init__(self, obj, powered, color):
        self.obj = obj
        self.name = self.obj.name + 'word'
        self.powered = powered
        self.color = color
        self.eff = {'PUSH'}
        self.type = 'subj'
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f'{self.name}'

class eq: #includes just the word 'IS' for making rules
    def __init__(self, subj, descriptor, powered, color):
        self.name = 'is'
        self.subj= subj
        self.desc= descriptor
        self.powered = powered
        self.color = color
        self.eff = {'PUSH'}
        self.type = 'eq'
        
    def makeSubject(self, other):
        self.subj = other
        
    def makeDescribe(self, other):
        if isinstance(other, effect):
            self.desc = other.desc
        
    def makeRule(self):
        if self.subj != None and self.desc != None:
            self.subj.addEffect(self.desc)
        
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return f'{self.name}'
        
class effect: #includes (YOU, STOP, MELT, SINK, WIN)
    def __init__(self, desc, powered, color):
        self.desc = desc
        self.powered = powered
        self.color = color
        self.eff = {'PUSH'}
        self.type = 'effect'
        
    def __hash__(self):
        return hash(self.desc)
    
    def __repr__(self):
        return f'{self.desc}'


class adj: #includes (NOT, AND)
    pass

#map and level---------------
class level: 
    def __init__(self, num, dict, wd):
        self.num = num
        self.dict = dict
        self.wd = wd
        self.rules = []
    
          
        
#(!!) REPLACE THESE ALL WITH SUBCLASSES! 
#List of objects in game
baba = obj('BABA', 'right', 'lightGrey','white')
rock = obj('ROCK', 'right', 'saddleBrown', 'white')
wall = obj('WALL', 'right', 'dimGrey','white')
flag = obj('FLAG', 'right', 'gold','white')

#instance of 'IS' class
equals = eq(None, None, False, 'black')

#List of subjects in game. Copy the subject classes to implement multiple instances in a game
babaw = subj(baba, False, 'grey')
rockw = subj(rock, False, 'saddleBrown')
wallw = subj(wall, False, 'dimGrey')
flagw = subj(flag, False, 'gold')

#List of effects in game
you = effect('YOU', False,'black')
push = effect('PUSH', False,'black')
stop = effect('STOP', False, 'black')
win = effect('WIN', False, 'gold')
