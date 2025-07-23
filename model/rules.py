import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.lookup import *

def getRules(level):
    rules = []
    for item in level.dict:
        if isinstance(item, obj) and item.eff != []:
            for effect in item.eff:  
                rules += [(item,effect)]
    return rules
    
def makeRules(level): 
    for (word, (subjectWord, effectWord)) in level.rules:
        #apply effects to objects
        if isinstance(effectWord,effect):
            word.makeSubject(subjectWord)
            word.makeDescribe(effectWord)
            word.makeRule()
            
        #SUBJ IS SUBJ replaces objects
        elif isinstance(effectWord, obj):
            currSet = level.dict[effectWord]
            newSet = level.dict[subjectWord]
            level.dict[effectWord] = currSet | newSet
            level.dict[subjectWord] = set()
        word.powered = subjectWord.powered = effectWord.powered = True
        
def delRules(level):
    checkList = [itemRuleTuple for (equals, itemRuleTuple) in level.rules]
    for item in level.dict:
        if isinstance(item,obj):
            itemRules = item.eff
            for rule in itemRules: 
                check = (item, rule)
                if check not in checkList:
                    itemRules.remove(rule)
            
    
def compileRules(level):
    #initialize a rules tuple list to store rules in play, AS LISTED BY WORDS ON BOARD.
    rules = []
    
    #we need to get the list of 'IS' instances first.
    equalsSet = getEquals(level.wd)
    levelDict = level.dict
    
    for word in equalsSet: 
        #identify target cells to check. Rules can only be made in the following configs:
        #          SUBJECT
        # SUBECT     IS     EFFECT
        #          EFFECT
        #So we check the cell above and left of 'IS' for subject, and so on. 
        for coord in levelDict[word]:
            #should ever only run once, unless we want linked words for some reason
            coordX, coordY = coord
            horiSubjCoord = (coordX - 1, coordY)
            vertiSubjCoord = (coordX, coordY-1)
            horiEffCoord = (coordX + 1, coordY)
            vertiEffCoord = (coordX, coordY+1)
            
        #make the checklist to check in subject-effect pairs. coords are tuples. 
        checkList = [(horiSubjCoord,horiEffCoord),(vertiSubjCoord,vertiEffCoord)]
        
        #check for each "IS" instance 
        for pair in checkList:
            subjCell, effCell = pair 
        
            #Check if a subject and effect word is present
            if (findClass(levelDict, subjCell, 'subj') 
                and findClass(levelDict, effCell, 'effect')): 
                #define subject and object for the makeRule function
                subjectWord = findClass(levelDict, subjCell, 'subj').obj
                effectWord = findClass(levelDict, effCell, 'effect')
                rules += [(word, (subjectWord, effectWord))] 
            elif (findClass(levelDict, subjCell, 'subj') 
                  and findClass(levelDict, effCell, 'subj')): 
                subjectWord = findClass(levelDict, subjCell, 'subj').obj
                effectWord = findClass(levelDict, effCell, 'subj').obj
                rules += [(word, (subjectWord, effectWord))]     
            else:
                pass    
    return rules

def refreshRules(level):
    level.rules = compileRules(level)
    delRules(level)
    makeRules(level)  