import re
import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from model.objects import *
from model.lookup import *
from sounds.sounds import *
from model.movement import *

#rule compiling and execution--------------------------------

def makeCheckCoordinates(coord):
    coordX, coordY = coord
    horiSubjCoord = (coordX - 1, coordY)
    vertiSubjCoord = (coordX, coordY-1)
    horiEffCoord = (coordX + 1, coordY)
    vertiEffCoord = (coordX, coordY+1)
    return [(horiSubjCoord, horiEffCoord), (vertiSubjCoord, vertiEffCoord)]

def compileRules(app):
    #initialize a rules tuple list to store rules in play, AS LISTED BY WORDS ON BOARD.
    rules = []
    
    #get all equators and logical operators
    equalsSet = getEquals(app)
    for word in equalsSet: 
        if word.attribute == 'equals': #evaluate the 'IS' statements first. 
            #identify target cells to check. Rules can only be made in the following configs:
            #          SUBJECT
            # SUBECT     IS     EFFECT
            #          EFFECT
            #So we check the cell above and left of 'IS' for subject, and so on. 
            checkList = makeCheckCoordinates(app.levelDict[word])
            
            #check for each "IS" instance 
            for pair in checkList:
                subjCell, effCell = pair 
                subjWord = findClass(app, subjCell, 'subj')
                effWord = findClass(app, effCell, 'effect')
                swapWord = findClass(app, effCell, 'subj')
                #Check if a subject and effect word is present:
                #this is SUBJECT IS EFFECT case
                if subjWord and effWord:
                    rules.insert(1,(word, (subjWord, effWord)))
                    effWord.rootSubj = subjWord
                    subjWord.rootEffect = effWord
                
                #go into swap object case
                elif subjWord and swapWord: 
                    rules.insert(1,(word, (subjWord, swapWord)))
                    swapWord.rootSubj = subjWord
                else: #got nothing
                    pass    
                
        elif word.attribute == 'and': #then we evaluate the AND statements. 
            #identify target cells to check. AND conjunctions can only be made in the following configs:
            #          SUBJECT
            # SUBECT     IS     EFFECT AND SUBJECT / EFFECT
            #          EFFECT
            #          AND
            #     SUBJECT / EFFECT
            #we need a rootSubject value for each subject and effect in an 'IS' statement.
            #Then, all 'AND' need does is read whether its subject is powered, 
            #and act like an 'IS' statement for the root subject of the subject. 
            checkList = makeCheckCoordinates(app.levelDict[word])
            for pair in checkList:
                subjCell, effCell = pair
                appliedSubjWord = findClass(app, subjCell, 'subj')
                appliedEffWord = findClass(app, subjCell, 'effect')
                applyingEffWord = findClass(app, effCell, 'effect')
                applyingSubjWord = findClass(app, effCell, 'subj')
                if ((applyingSubjWord and applyingSubjWord.powered)): #inserting the AND statement before an 'IS' statement. 
                    #e.g. KIMCHI AND BABA IS HOT: breaks down into KIMCHI IS HOT and BABA IS HOT
                    #e.g. KIMCHI AND BABA IS MELT AND SINK: KIMCHI IS MELT, KIMCHI IS SINK, same thing for BABA
                    #e.g. 
                    #takeaway: we apply the applied effect to the ROOT subject. 
                    if appliedSubjWord:
                        applyingSubjWord.rootSubj = appliedSubjWord
                        word.rootSubj = applyingSubjWord
                        rules.append((word, (appliedSubjWord, applyingSubjWord.rootEffect)))
                    
                elif ((appliedSubjWord and appliedSubjWord.rootSubj)
                    or (appliedEffWord and appliedEffWord.rootSubj)): #inserting the AND statement after an 'IS' statement. 
                    #e.g. KIMCHI IS BABA AND HOT: breaks down into KIMCHI IS BABA and KIMCHI IS HOT
                    #e.g. KIMCHI IS BABA AND KEKE: breaks down into KIMCHI IS BABA and KIMCHI IS KEKE
                    #e.g. KIMCHI IS HOT AND BABA: breaks down into KIMCHI IS HOT and KIMCHI IS BABA
                    #e.g. KIMCHI IS HOT AND MELT: breaks down into KIMCHI IS HOT and KIMCHI IS MELT
                    #takeaway: we apply the applied effect to the ROOT subject. 
                    subject = appliedSubjWord.rootSubj if appliedSubjWord else appliedEffWord.rootSubj  
                    appliedEffect = applyingSubjWord if applyingSubjWord else applyingEffWord
                    
                    #must be applied LAST for the IS statements to properly establsih roots
                    if appliedEffect:
                        rules.append((word, (subject, appliedEffect)))
                        if subject.rootSubj:
                            rules.append((word, (subject.rootSubj, appliedEffect)))
                        if applyingEffWord:
                            applyingEffWord.rootSubj = subject
                        elif applyingSubjWord:
                            applyingSubjWord.rootSubj = subject
                        word.rootSubj = subject
                else:
                    pass
        elif word.attribute == 'not': #finally we work on negation.
            pass #(to be done later)
    return rules
    
def makeRules(app): #main function that calls helpers to apply new rules
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

def addEffects(app, subjectWord, effectWord): #adds effect to subject
    appendType = subjectWord.obj
    for object in app.levelDict:
        if (isinstance(object, obj) #item is an object 
            and object.attribute == appendType #item matches type
            and effectWord.attribute not in object.effectsList): #effect hasn't been appended alr
                    #apply effects to objects
                object.effectsList.append(effectWord.attribute) 

def checkPower(app):
    wordCheckList = ruleUnpacker(app.levelRules)
    for item in app.levelDict:
        if (isinstance(item, effect) 
                or isinstance(item, subj) 
                or isinstance(item, eq)):
                if item in wordCheckList:
                    if item.attribute == 'and':
                        if item.rootSubj and not item.rootSubj.powered:
                            item.powered = False
                            continue
                    item.powered = True
                else:
                    item.powered = False
                    
def delRules(app): #main function that deletes old rules no longer in play
    checkList = [itemRuleTuple for (equals, itemRuleTuple) in app.levelRules]
    for item in app.levelDict:
        if item.attribute != 'cursor':
            if isinstance(item, obj):
                itemRules = item.effectsList
                for rule in itemRules: 
                    check = (item, rule)
                    if check not in checkList:
                        itemRules.remove(rule)
                
#Replacement-related rules--------------------------------
def replaceObjs(app, subjectWord, effectWord):
    appendType = subjectWord.obj
    replaceType = effectWord.obj
    objPairs = {(subjectWord.attribute, effectWord.attribute)
        for (word, (subjectWord, effectWord)) in app.levelRules 
        if word.attribute == 'equals'}
    if (subjectWord.attribute, subjectWord.attribute) in objPairs: #KIMCHI IS KIMCHI overrides any other replacement rules.
        return
    for object in app.levelDict:
        if (isinstance(object, obj) 
            and object.attribute == appendType):
            object.setAttribute(replaceType)
            object.effectsList = copy.deepcopy(findLookupList(app, replaceType))
            #record the type change for undo / reset
            app.turnMoves.append((object, appendType, replaceType))

#for the BS 'ROCK IS WALL IS ROCK IS WALL IS ROCK' edge case.
#if ROCK IS WALL IS ROCK, then all WALLS alternate between being ROCKS and WALLS every turn, and same for ROCKS.
def swapObjs(app): 
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
def deleteBoard(app):
    sinkList = []
    defeatList = []
    meltList = []
    openList = []
    for object in app.levelDict:
        if 'sink' in object.effectsList:
            sinkList.append((object, object.pos))
        elif 'defeat' in object.effectsList:
            defeatList.append((object, object.pos))
        elif 'melt' in object.effectsList:
            meltList.append((object, object.pos))
        elif 'open' in object.effectsList:
            openList.append((object, object.pos))
    sinkObjs(app, sinkList)
    defeatObjs(app, defeatList)
    meltObjs(app, meltList)
    openObjs(app, openList)
            
def deleteObject(app, object): #call this on sink, defeat, hot/melt, XX IS empty. 
    if object.preSink:
        prevCell = object.preSink
    else:
        prevCell = object.pos
    app.levelDict.pop(object)
    app.turnMoves.append((object, object.type, object.effectsList, object.attribute, prevCell))
        
def sinkObjs(app, sinkList): #sink object remove function (kills everything not FLOAT in its cell)
    sinkedObject = False
    for (sinkObject, cell) in sinkList:
        if cell and len(getObjectsInCell(app, *cell)) > 1: 
            #if theres more than one object in the cell, we delete everything in the cell
            for objectToSink in getObjectsInCell(app, *cell):
                if ('float' not in objectToSink.effectsList
                    or 'float' in sinkObject.effectsList): #FLOAT objects only check each other.
                    deleteObject(app, objectToSink)
                    sinkedObject = True
                    app.turnMoves.append((objectToSink, objectToSink.type, objectToSink.effectsList, objectToSink.attribute, cell))
                    
    if sinkedObject:
        playRandomSinkSound()

def defeatObjs(app, defeatList): #defeat object remove function 
    defeatedObject = False
    for (defeatObject, cell) in defeatList:
        playerObject = findObj(app, cell, 'you')
        if playerObject:
            if ('float' not in playerObject.effectsList
                or 'float' in defeatObject.effectsList): #FLOAT objects only check each other.
                deleteObject(app, playerObject)
                defeatedObject = True
                app.turnMoves.append((playerObject, playerObject.type, playerObject.effectsList, playerObject.attribute, cell))
                
    if defeatedObject:
        playRandomDefeatSound()

def meltObjs(app, meltList): #melt object remove function (kills everything not FLOAT in its cell)
    meltedObject = False
    for (hotObject, cell) in meltList:
        meltObject = findObj(app, cell, 'melt')
        if meltObject:
            if ('float' not in meltObject.effectsList
                or 'float' in hotObject.effectsList): #FLOAT objects only check each other.
                deleteObject(app, meltObject)
                meltedObject = True
                app.turnMoves.append((meltObject, meltObject.type, meltObject.effectsList, meltObject.attribute, cell))
                
    if meltedObject:
        playRandomMeltSound()

def openObjs(app, openList): #open object remove function
    openedObject = False
    for (shutObject, cell) in openList:
        if cell and len(getObjectsInCell(app, *cell)) > 1:
            for keyObject in getObjectsInCell(app, *cell):
                if 'open' in keyObject.effectsList:
                    deleteObject(app, keyObject)
                    deleteObject(app, shutObject)
                    openedObject = True
                    app.turnMoves.append((shutObject, shutObject.type, shutObject.effectsList, shutObject.attribute, cell))
                    break
                else:
                    continue
                    
    if openedObject:
        playRandomOpenSound()

#reset functions--------------------------------
def resetLevel(app):
    #create a list of items before iterating to avoid dictionary modification during iteration
    app.levelDict = copy.deepcopy(app.level.dict)
    items = list(app.levelDict.keys()) #copy the original file
    for item in items:
        item.resetPos()
        app.levelDict[item] = item.pos
        item.attribute = item.initialState
    app.moveHistory = []
    app.turnMoves = []
    app.replaceCount = 0
    refreshRules(app)
    
    # Just update rules without checking win state
    app.levelRules = compileRules(app)
    delRules(app)
    makeRules(app)
    
    # Update players
    app.players = getPlayer(app)
    app.noPlayer = len(app.players) == 0

#refresh function here for global access to everything
def refresh(app):
    #rule refresh   
    refreshRules(app)
    swapObjs(app)
    deleteBoard(app)
    autoMoveObjs(app)
    refreshRules(app)
    
    #move logging
    if app.turnMoves: #don't want to store empty stacks
        app.moveHistory += [app.turnMoves]
    if app.debugMode: 
        print('\n')
        print('-------')
        print('moves made this turn:', app.turnMoves)
        print('-------')
    app.turnMoves = []

    #update game state
    app.players = getPlayer(app)
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
        checkWin(app, app.levelDict)  # Only check for win if we have players
        
def undoRefreshHelper(app):
    #rule refresh   
    refreshRules(app)
    swapObjs(app)
    deleteBoard(app)
    refreshRules(app)
    
    if app.debugMode: 
        print('\n')
        print('-------')
        print('undone moves:', app.turnMoves)
        print('-------')
    app.turnMoves = []

    #update game state
    app.players = getPlayer(app)
    if len(app.players) == 0:
        app.noPlayer = True
    else:
        app.noPlayer = False
        checkWin(app, app.levelDict)  # Only check for win if we have players
    

def refreshRules(app):
    checkPower(app)
    app.levelRules = compileRules(app)
    delRules(app)
    makeRules(app)
    app.levelRules = compileRules(app)
def ruleUnpacker(list):
    returnList = []
    for tuple in list:
        equals, (itemWord, effectWord) = tuple
        if equals.attribute == 'and': #this ensures the 'AND' statement is looked at last
            #so game can accurately grab powered state of the words around it. 
            returnList.append(equals)
        else:
            returnList.insert(0, equals)
        returnList.insert(0, itemWord)
        returnList.insert(0, effectWord)
    return returnList

def undoMove(app):
    if len(app.moveHistory) == 0: #no moves to undo
        return None
    else:
        moveStack = app.moveHistory.pop()
        for move in moveStack[::-1]:
            if len(move) == 2: #this means tuple is a move
                if app.debugMode:
                    print('recovering move')
                (object, direction) = move
                #could be better implementation for this lmao
                (object, direction) = move
                object.undoMove()
                app.levelDict[object] = object.pos #this is the only place we write to the levelDict
            elif len(move) == 3: #this means tuple is a type change
                if app.debugMode:
                    print('recovering type change')
                (object, oldType, newType) = move
                object.setAttribute(oldType)
            elif len(move) == 5: #this means tuple is a deletion
                if app.debugMode:
                    print('recovering deletion')
                (object, type, effectsList, attribute, cell) = move
                object.pos = cell
                app.levelDict[object] = cell
                object.attribute = attribute
                object.effectsList = effectsList
                if 'defeat' in effectsList:
                    object.effectsList.remove('defeat')
                elif 'melt' in effectsList and 'hot' in effectsList:
                    object.effectsList.remove('melt')
                object.type = type
    undoRefreshHelper(app)
        