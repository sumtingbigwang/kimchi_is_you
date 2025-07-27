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
    doubleReplaced = False
    rulePairs = []
    for (word, (subjectWord, effectWord)) in level.rules:
        rulePairs += [(subjectWord, effectWord)]
    
    for pair in rulePairs:
        subjectWord, effectWord = pair
        if isinstance(subjectWord, subj) and isinstance(effectWord, effect):
            addEffects(app, level, subjectWord, effectWord)
        #SUBJ IS SUBJ replaces objects
        elif isinstance(subjectWord, subj) and isinstance(effectWord, subj):
            replaceObjs(app, level, subjectWord, effectWord)
            

def addEffects(app, level, subjectWord, effectWord):
    appendType = subjectWord.obj
    for object in level.dict:
        if (isinstance(object, obj) #item is an object 
            and object.attribute == appendType #item matches type
            and effectWord.attribute not in object.effectsList): #effect hasn't been appended alr
                    #apply effects to objects
                object.effectsList.append(effectWord.attribute) 
                
def replaceObjs(app, level, subjectWord, effectWord):
    appendType = subjectWord.obj
    replaceType = effectWord.obj
    for object in level.dict:
        if (isinstance(object, obj) and object.attribute == appendType):
            object.setAttribute(replaceType)
            object.effectsList = copy.deepcopy(findLookupList(level.dict, replaceType))
            #record the type change for undo / reset
            app.turnMoves.append((object, appendType, replaceType))
        
def swapObjs(app, level):
    replaceObjPairs = []
    objPairs = [(subjectWord, effectWord)
        for (word, (subjectWord, effectWord)) in level.rules 
        if word.attribute == 'equals'] 
    attributePairs = [(subjectWord.attribute, effectWord.attribute)
                      for (subjectWord, effectWord) in objPairs]
    
    for lIdx in range(len(attributePairs)):
        invertedPair = attributePairs[lIdx][::-1]
        if invertedPair in attributePairs:
            replaceObjPairs += [objPairs[lIdx]]
            attributePairs[lIdx] = ('bogo','bogo')
            
    for pair in replaceObjPairs:
        subjectWord, effectWord = pair
        replaced = subjectWord.attribute
        replacement = effectWord.attribute
        if app.replaceCount % 2 == 0:
            replaceObjs(app, level, pair[0], pair[1])
        elif app.replaceCount % 2 == 1:
            replaceObjs(app, level, pair[1], pair[0])
        app.replaceCount += 1
    
                    
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
        if item.attribute != 'cursor':
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
    level.rules = compileRules(level)
    delRules(level)
    getRules(level)
    makeRules(app,level)
    swapObjs(app, level)
    
    #move logging
    if app.turnMoves: #don't want to store empty stacks
        app.moveHistory += [app.turnMoves]
    app.turnMoves = []

    #update game state
    app.players = getPlayer(app.level)
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
        checkWin(app, app.levelDict)  # Only check for win if we have players
    