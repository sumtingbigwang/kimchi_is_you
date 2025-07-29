import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.lookup import *
from sounds.sounds import *

#rule compiling and execution--------------------------------
def compileRules(app):
    #initialize a rules tuple list to store rules in play, AS LISTED BY WORDS ON BOARD.
    rules = []
    
    #we need to get the list of 'IS' instances first.
    equalsSet = getEquals(app)
    equalsNames = [word.name for word in equalsSet]
    for word in equalsSet: 
        #identify target cells to check. Rules can only be made in the following configs:
        #          SUBJECT
        # SUBECT     IS     EFFECT
        #          EFFECT
        #So we check the cell above and left of 'IS' for subject, and so on. 
        coord = app.levelDict[word]
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
            if (findClass(app, subjCell, 'subj') 
                and findClass(app, effCell, 'effect')): 
                #define subject and object for the makeRule function
                subjectWord = findClass(app, subjCell, 'subj')
                effectWord = findClass(app, effCell, 'effect')
                rules += [(word, (subjectWord, effectWord))] 
            elif (findClass(app, subjCell, 'subj') 
                  and findClass(app, effCell, 'subj')): 
                subjectWord = findClass(app, subjCell, 'subj')
                effectWord = findClass(app, effCell, 'subj')
                rules += [(word, (subjectWord, effectWord))]     
            else:
                pass    
    return rules
def getRules(app):
    rules = []
    for item in app.levelDict:
        if isinstance(item, obj) and item.effectsList != []:
            for effect in item.effectsList:  
                rules += [(item,effect)]
    return rules
    
def makeRules(app): 
    rulePairs = []
    for (word, (subjectWord, effectWord)) in app.levelRules:
        rulePairs += [(subjectWord, effectWord)]
    
    for pair in rulePairs:
        subjectWord, effectWord = pair
        if isinstance(subjectWord, subj) and isinstance(effectWord, effect):
            addEffects(app, subjectWord, effectWord)
        #SUBJ IS SUBJ replaces objects
        elif isinstance(subjectWord, subj) and isinstance(effectWord, subj):
            replaceObjs(app, subjectWord, effectWord)

                    
def delRules(app):
    checkList = [itemRuleTuple for (equals, itemRuleTuple) in app.levelRules]
    wordCheckList = ruleUnpacker(app.levelRules)

    for item in app.levelDict:
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
            
def addEffects(app, subjectWord, effectWord):
    appendType = subjectWord.obj
    for object in app.levelDict:
        if (isinstance(object, obj) #item is an object 
            and object.attribute == appendType #item matches type
            and effectWord.attribute not in object.effectsList): #effect hasn't been appended alr
                    #apply effects to objects
                object.effectsList.append(effectWord.attribute) 
                
#Replacement-related rules--------------------------------
def replaceObjs(app, subjectWord, effectWord):
    appendType = subjectWord.obj
    replaceType = effectWord.obj
    for object in app.levelDict:
        if (isinstance(object, obj) and object.attribute == appendType):
            object.setAttribute(replaceType)
            object.effectsList = copy.deepcopy(findLookupList(app, replaceType))
            #record the type change for undo / reset
            app.turnMoves.append((object, appendType, replaceType))
        
def swapObjs(app): #for the BS 'ROCK IS WALL IS ROCK IS WALL IS ROCK' edge case
    replaceObjPairs = []
    objPairs = [(subjectWord, effectWord)
        for (word, (subjectWord, effectWord)) in app.levelRules 
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
            replaceObjs(app, pair[0], pair[1])
        elif app.replaceCount % 2 == 1:
            replaceObjs(app, pair[1], pair[0])
        app.replaceCount += 1
        
#Deletion-related rules--------------------------------
def deleteObject(app, object):
    if object.preSink:
        prevCell = object.preSink
    else:
        prevCell = object.pos
    app.levelDict.pop(object)
    app.turnMoves.append((object, object.type, object.effectsList, object.attribute, prevCell))
        
def sinkObjs(app):
    sinkObjs = [sinkObject for sinkObject in app.levelDict if 'sink' in sinkObject.effectsList]
    sinkCells = [sinkObject.pos for sinkObject in sinkObjs]
    for cell in sinkCells:
        if cell and len(getObjectsInCell(app, *cell)) > 1: 
            playRandomSinkSound()
            #if theres more than one object in the cell, we delete everything in the cell
            for sinkObject in getObjectsInCell(app, *cell):
                deleteObject(app, sinkObject)

def defeatObjs(app):
    defeatObjs = [defeatObject for defeatObject in app.levelDict if 'defeat' in defeatObject.effectsList]
    defeatCells = [defeatObject.pos for defeatObject in defeatObjs]
    for cell in defeatCells:
        playerObject = findObj(app, cell, 'you')
        if playerObject:
            playRandomDefeatSound()
            deleteObject(app, playerObject)

#helper functions--------------------------------
def executeRules(app):
    app.levelRules = compileRules(app)
    delRules(app)
    getRules(app)
    makeRules(app)

def refresh(app):
    #rule refresh   
    executeRules(app)
    swapObjs(app)
    sinkObjs(app)
    defeatObjs(app)
    
    #move logging
    if app.turnMoves: #don't want to store empty stacks
        app.moveHistory += [app.turnMoves]
    if app.debugMode: 
        print('moves made this turn:', app.turnMoves)
    app.turnMoves = []

    #update game state
    app.players = getPlayer(app)
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
        checkWin(app, app.levelDict)  # Only check for win if we have players
    
def ruleUnpacker(list):
    returnList = set()
    for tuple in list:
        equals, (itemWord, effectWord) = tuple
        returnList.add(equals)
        returnList.add(itemWord)
        returnList.add(effectWord)
    return returnList
        