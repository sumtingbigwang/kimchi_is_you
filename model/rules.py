import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.lookup import *

def getRules(level):
    rules = []
    for item in level.dict:
        if isinstance(item, obj) and item.effectsList != []:
            for effect in item.effectsList:  
                rules += [(item,effect)]
    return rules
    
def makeRules(app,level): 
    for (word, (subjectWord, effectWord)) in level.rules:
        appendType = subjectWord.obj
        if isinstance(subjectWord, subj) and isinstance(effectWord, effect):
            for object in level.dict:
                if (isinstance(object, obj) #item is an object 
                    and object.attribute == appendType #item matches type
                    and effectWord.attribute not in object.effectsList): #effect hasn't been appended alr
                            #apply effects to objects
                            object.effectsList.append(effectWord.attribute) 
                            
        #SUBJ IS SUBJ replaces objects
        if isinstance(subjectWord, subj) and isinstance(effectWord, subj):
            replaceType = effectWord.obj
            for object in level.dict:
                if (isinstance(object, obj) and object.attribute == appendType):
                    object.setAttribute(replaceType)
                    #record the type change for undo / reset
                    app.turnMoves.append((object, appendType, replaceType))
                    
def ruleUnpacker(list):
    returnList = set()
    for tuple in list:
        equals, (itemWord, effectWord) = tuple
        returnList.add(equals)
        returnList.add(itemWord)
        returnList.add(effectWord)
    return returnList
        
                    
def delRules(level):
    checkList = [itemRuleTuple for (equals, itemRuleTuple) in level.rules]
    wordCheckList = ruleUnpacker(level.rules)

    for item in level.dict:
        if isinstance(item, obj):
            itemRules = item.effectsList
            for rule in itemRules: 
                check = (item, rule)
                if check not in checkList:
                    itemRules.remove(rule)

        elif (isinstance(item, effect) 
              or isinstance(item, subj) 
              or isinstance(item, eq)):
            if item in wordCheckList:
                item.powered = True
            else:
                item.powered = False
            
            
    
def compileRules(level):
    #initialize a rules tuple list to store rules in play, AS LISTED BY WORDS ON BOARD.
    rules = []
    
    #we need to get the list of 'IS' instances first.
    equalsSet = getEquals(level.dict)
    equalsNames = [word.name for word in equalsSet]
    levelDict = level.dict
    for word in equalsSet: 
        #identify target cells to check. Rules can only be made in the following configs:
        #          SUBJECT
        # SUBECT     IS     EFFECT
        #          EFFECT
        #So we check the cell above and left of 'IS' for subject, and so on. 
        coord = level.dict[word]
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
                subjectWord = findClass(levelDict, subjCell, 'subj')
                effectWord = findClass(levelDict, effCell, 'effect')
                rules += [(word, (subjectWord, effectWord))] 
            elif (findClass(levelDict, subjCell, 'subj') 
                  and findClass(levelDict, effCell, 'subj')): 
                subjectWord = findClass(levelDict, subjCell, 'subj')
                effectWord = findClass(levelDict, effCell, 'subj')
                rules += [(word, (subjectWord, effectWord))]     
            else:
                pass    
    return rules

def refresh(app,level):
    #rule refresh 
    level.rules = compileRules(level) #first read all rules on screen made by words.
    getRules(level) #then store all rules in level.rules for printing. 
    delRules(level) #we cross-check level.rules for rules removed, and delete extra rules from objects.
    makeRules(app,level) #we THEN check for new rules made and apply them 
    #move logging
    #cache all moves made this turn, put it in a stack that can be executed on one button press.
    if app.turnMoves: #don't want to store empty stacks
        app.level.moveHistory += [app.turnMoves] #'your mom could be a stack' --seunghyeok lee
    #now reset turn moves for the next action done. 
    app.turnMoves = []
    