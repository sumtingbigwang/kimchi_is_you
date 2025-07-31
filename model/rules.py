from math import atan
import re
import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics.shape_logic import checkNonNegative
from model.objects import *
from model.lookup import *
from sounds.sounds import *
from levels import *
from model.movement import *

#rule compiling and execution--------------------------------

def checkEquals(app, word, rules):
                #identify target cells to check. Rules can only be made in the following configs:
            #          SUBJECT
            # SUBECT     IS     EFFECT
            #          EFFECT
            #So we check the cell above and left of 'IS' for subject, and so on. 
            checkList = makeCheckCoordinates(app.levelDict[word], 'is')
            
            #check for each "IS" instance 
            for pair in checkList:
                subjCell, effCell = pair 
                subjWord = findClass(app, subjCell, 'subj')
                effWord = findClass(app, effCell, 'effect')
                swapWord = findClass(app, effCell, 'subj')
                notWord = findClass(app, effCell, 'not')
                #Check if a subject and effect word is present:
                #this is SUBJECT IS EFFECT case
                if subjWord:
                    word.rootSubj = subjWord
                    subjWord.rootOperator = word
                    if effWord:
                        if subjWord.attribute == 'level':
                            rules.insert(3,(word, (subjWord, effWord)))
                        else:
                            rules.insert(0,(word, (subjWord, effWord)))
                        effWord.rootSubj = subjWord
                        subjWord.rootEffect = effWord
                        subjWord.rootOperator = word
                        word.rootEffect = effWord
                
                #go into swap object case
                    elif swapWord: 
                        rules.insert(0,(word, (subjWord, swapWord)))
                        swapWord.rootSubj = subjWord
                        word.rootEffect = swapWord
                    elif notWord:
                        if notWord.rootEffect:
                            word.rootEffect = notWord
                    else: #got nothing
                        word.rootEffect = None
                
def checkAnd(app, word, rules):
    #identify target cells to check. AND conjunctions can only be made in the following configs:
            #          SUBJECT
            # SUBECT     IS     EFFECT AND SUBJECT / EFFECT
            #          EFFECT
            #          AND
            #     SUBJECT / EFFECT
            #we need a rootSubject value for each subject and effect in an 'IS' statement.
            #Then, all 'AND' need does is read whether its subject is powered, 
            #and act like an 'IS' statement for the root subject of the subject. 
            checkList = makeCheckCoordinates(app.levelDict[word], 'and/not')
            for pair in checkList:
                subjCell, effCell, eoCell, soCell = pair
                appliedSubjWord = findClass(app, subjCell, 'subj')
                applyingSubjWord = findClass(app, effCell, 'subj')
                appliedEffWord = findClass(app, subjCell, 'effect')
                applyingEffWord = findClass(app, effCell, 'effect')
                applyingNot = findClass(app, effCell, 'not')
                applyingEO = findClass(app, eoCell, 'eq')
                if (applyingSubjWord 
                     and applyingSubjWord.rootOperator
                     and applyingSubjWord.rootOperator.powered): #inserting the AND statement before an 'IS' statement. 
                    #e.g. KIMCHI AND BABA IS HOT: breaks down into KIMCHI IS HOT and BABA IS HOT
                    #e.g. KIMCHI AND BABA IS MELT AND SINK: KIMCHI IS MELT, KIMCHI IS SINK, same thing for BABA
                    #e.g. 
                    #takeaway: we apply the applied effect to the ROOT subject. 
                    if appliedSubjWord:
                        applyingSubjWord.rootSubj = appliedSubjWord
                        word.rootSubj = applyingSubjWord
                        rules.insert(-2,(word, (appliedSubjWord, applyingSubjWord.rootEffect)))
                    elif applyingNot:
                        word.rootSubj = applyingSubjWord
                    
                elif ((appliedSubjWord and appliedSubjWord.rootSubj and appliedSubjWord.powered)
                    or (appliedEffWord and appliedEffWord.rootSubj and appliedEffWord.powered)): 
                    #inserting the AND statement after an 'IS' statement. 
                    #e.g. KIMCHI IS BABA AND HOT: breaks down into KIMCHI IS BABA and KIMCHI IS HOT
                    #e.g. KIMCHI IS BABA AND KEKE: breaks down into KIMCHI IS BABA and KIMCHI IS KEKE
                    #e.g. KIMCHI IS HOT AND BABA: breaks down into KIMCHI IS HOT and KIMCHI IS BABA
                    #e.g. KIMCHI IS HOT AND MELT: breaks down into KIMCHI IS HOT and KIMCHI IS MELT
                    #takeaway: we apply the applied effect to the ROOT subject. 
                    subject = appliedSubjWord.rootSubj if appliedSubjWord else appliedEffWord.rootSubj  
                    appliedEffect = applyingSubjWord if applyingSubjWord else applyingEffWord
                    
                    #must be applied LAST for the IS statements to properly establsih roots
                    if appliedEffect:
                        rules.insert(-2,(word, (subject, appliedEffect)))
                        if subject.rootSubj:
                            rules.insert(-2,(word, (subject.rootSubj, appliedEffect)))
                        if applyingEffWord:
                            applyingEffWord.rootSubj = subject
                        elif applyingSubjWord:
                            applyingSubjWord.rootSubj = subject
                        word.rootSubj = subject
                else:
                    pass

def checkNot(app, word, rules):
    chainNegated = False
    singleNegated = False
    operatorNegated = False
    # KIMCHI NOT ON ROCK IS HOT (negate operator, really only works for the 'ON' operator.)
    # KIMCHI AND NOT BABA IS HOT (negate AND operator)
    checkList = makeCheckCoordinates(app.levelDict[word], 'and/not')
    for tuple in checkList:
        subjCell, effCell, eoCell, soCell = tuple
        frontSubject = findClass(app, subjCell, 'subj')
        frontOperator = findClass(app, subjCell, 'eq')
        negatedSubject = findClass(app, effCell, 'subj')
        negatedSubjectOperator = findClass(app, eoCell, 'eq')
        negatedEffect = findClass(app, effCell, 'effect')
        doubleNegation = (findClass(app, soCell, 'eq') 
                          if findClass(app, soCell, 'eq') 
                          and findClass(app, soCell, 'eq').attribute == 'not' 
                          else None)
        negatedOperator = (findClass(app, effCell, 'eq') 
                           if findClass(app, effCell, 'eq')
                           and findClass(app, effCell, 'eq').attribute == 'on'
                           else None) #do this because we don't want NOT to start negating the IS operator. 
        
        if negatedSubject: # NOT KIMCHI IS HOT/ KIMCHI IS NOT BABA (negate subject)
            if frontOperator and frontOperator.rootSubj: #KIMCHI IS NOT BABA
                #in this case, the front operator isn't gonna be powered, so we check for root subject.
                word.rootSubj = frontOperator.rootSubj
                rules.insert(-2,(word, (frontOperator.rootSubj, negatedSubject))) 
                chainNegated = True
                
            elif (negatedSubject.powered 
                  and negatedSubjectOperator
                  and negatedSubjectOperator.powered
                  and negatedSubjectOperator.rootEffect): #NOT KIMCHI IS HOT
                if negatedSubjectOperator.attribute == 'equals':
                    word.rootSubj = negatedSubject
                    rules.append((word, (negatedSubject, negatedSubjectOperator.rootEffect)))
                    for subjectWord in app.levelDict:
                        if (isinstance(subjectWord, subj) 
                            and subjectWord != negatedSubject):
                            rules.insert(0,(negatedSubject.rootOperator, (subjectWord, negatedSubjectOperator.rootEffect)))
                            singleNegated = True
                    
        elif negatedEffect: # KIMCHI IS NOT HOT (negate effect)
            if frontOperator and frontOperator.rootSubj:
                if doubleNegation:
                    rules.append(('power', (word, doubleNegation)))
                else:
                    for subjectWord in app.levelDict:
                        if (isinstance(subjectWord, subj) 
                            and subjectWord != negatedEffect):
                            rules.append((word, (frontOperator.rootSubj, negatedEffect)))
                            #makeRules will read this and pop the rule if it's applied.
                            operatorNegated = True
                
        
                        
    if chainNegated:
        #append this tuple to tell checkPower to power up everything in the chain. 
        rules.append(('power', (word, frontOperator)))
        rules.append(('power', (frontOperator.rootSubj, negatedSubject)))
    if singleNegated:
        rules.append(('power', (word, word)))
    if operatorNegated:
        rules.append(('power', (frontOperator, word)))
        rules.append(('power', (negatedSubject, negatedEffect)))
        
def makeCheckCoordinates(coord, type):
    if type == 'is':
        coordX, coordY = coord
        horiSubjCoord = (coordX - 1, coordY)
        vertiSubjCoord = (coordX, coordY-1)
        horiEffCoord = (coordX + 1, coordY)
        vertiEffCoord = (coordX, coordY+1)
        return [(horiSubjCoord, horiEffCoord), (vertiSubjCoord, vertiEffCoord)]
    elif type == 'and/not':
        coordX, coordY = coord
        horiSubjCoord = (coordX - 1, coordY)
        vertiSubjCoord = (coordX, coordY-1)
        horiEffCoord = (coordX + 1, coordY)
        horiEOCoord = (coordX + 2, coordY) #EO for Effect Operator
        horiSOCoord = (coordX-3, coordY) #SO for subject operator (this is js for a NOT bug fix)
        vertiEffCoord = (coordX, coordY+1)
        vertiEOCoord = (coordX, coordY+2)
        vertiSOCoord = (coordX, coordY-3)
        return [(horiSubjCoord, horiEffCoord, horiEOCoord, horiSOCoord), (vertiSubjCoord, vertiEffCoord, vertiEOCoord, vertiSOCoord)]

def compileRules(app):
    #initialize a rules tuple list to store rules in play, AS LISTED BY WORDS ON BOARD.
    rules = []
    
    #get all equators and logical operators
    equalsSet = getEquals(app)
    for word in equalsSet: 
        if word.attribute == 'equals': #evaluate the 'IS' statements first. 
            checkEquals(app, word, rules)
            
        elif word.attribute == 'and': #then we evaluate the AND statements. 
            checkAnd(app, word, rules)
            
        elif word.attribute == 'not': #finally we work on negation.
            checkNot(app, word, rules)
    return rules #goes into app.levelRules
    
def makeRules(app): #main function that calls helpers to apply new rules
    rulePairs = []
    for (word, (subjectWord, effectWord)) in app.levelRules:
        if word == 'power':
            continue
        elif (word.attribute == 'equals' 
            or word.attribute == 'and'):
            rulePairs += [(subjectWord, effectWord)] #add rules
        elif word.attribute == 'not':
            elimSubject, elimWord = (subjectWord, effectWord)
            for (targetSubject, targetWord) in rulePairs:
                if (targetSubject.attribute == elimSubject.attribute
                    and targetWord.attribute == elimWord.attribute):
                    print('removing rule', targetSubject, targetWord)
                    rulePairs.remove((targetSubject, targetWord)) #remove rules negated by NOT
    
    for pair in rulePairs:
        subjectWord, effectWord = pair
        if (isinstance(subjectWord, subj) or subjectWord.attribute == 'level') and isinstance(effectWord, effect):
            addEffects(app, subjectWord, effectWord)
        #SUBJ IS SUBJ replaces objects
        elif isinstance(subjectWord, subj) and isinstance(effectWord, subj):
            replaceObjs(app, subjectWord, effectWord)

def addEffects(app, subjectWord, effectWord): #adds effect to subject
    if subjectWord.attribute == 'textword':
        for text in app.levelDict:
            if (isinstance(text, subj) 
                or isinstance(text, effect)
                or isinstance(text, eq)):
                    text.effectsList.append(effectWord.attribute)
                    
    if subjectWord.attribute == 'level':
        if effectWord.attribute == 'win':
            app.deadSound.pause()
            app.noPlayer = False
            app.levelWin = True
        elif effectWord.attribute == 'weak':
            app.levelGone = True
            if getFirstObject(app, 'you'):
                deleteObject(app, getFirstObject(app, 'you'))
        elif effectWord.attribute == 'hot':
            app.levelHot = True
            app.appendList = [item for item in app.levelDict if 'melt' in item.effectsList]
            app.levelDict = {item:item.pos for item in app.levelDict if 'melt' not in item.effectsList}
            for item in app.appendList:
                app.turnMoves.append((item, item.type, item.effectsList, item.attribute, item.pos))
        elif effectWord.attribute == 'defeat':
            app.appendList = [item for item in app.levelDict if 'you' in item.effectsList]
            app.levelDict = {item:item.pos for item in app.levelDict if 'you' not in item.effectsList}
            for item in app.appendList:
                app.turnMoves.append((item, item.type, item.effectsList, item.attribute, item.pos))
    else:
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
                    
def delRules(app): #main function that deletes old rules no longer in play and kills negated rules
    checkList = [itemRuleTuple for (equals, itemRuleTuple) in app.levelRules if equals != 'not on' and equals != 'power']
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
    if subjectWord.attribute == 'level':
        if app.levelNum == 21:
            mapItem = obj(f'O-13',f'{effectWord.obj}')
            mapItem.pos = (12,2)
            map.level.dict[mapItem] = (12,2)
        elif app.levelNum == 22 and effectWord.obj == 'flag':
            mapItem = obj(f'O-14','flag')
            mapItem.pos = (16,8)
            map.level.dict[mapItem] = (16,8)
        else:
            mapItem = obj(f'O-14',f'{effectWord.obj}')
            mapItem.pos = (2,5)
            map.level.dict[mapItem] = (2,5)
        app.metaMap = True
    appendType = subjectWord.obj
    replaceType = effectWord.obj
    objPairs = {(subjectWord.attribute, effectWord.attribute)
        for (word, (subjectWord, effectWord)) in app.levelRules 
        if not isinstance(word, str) and word.attribute == 'equals'}
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
        if (not isinstance(word, str)) and word.attribute == 'equals']
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
        
def moreObjs(app):
    moreCount = 0
    moreList = [object for object in app.levelDict if 'more' in object.effectsList]
    for object in moreList:
        objX, objY = object.pos
        moreSpaceList = [(objX+1,objY), (objX,objY+1), (objX-1,objY), (objX,objY-1)]
        for space in moreSpaceList:
            if len(getObjectsInCell(app,*(space))) < 1:
                moreObject = obj(f'O-{moreCount}',f'{object.attribute}')
                moreObject.pos = space
                app.levelDict[moreObject] = space
                moreCount +=1 
                
#Deletion-related rules--------------------------------
def deleteBoard(app):
    sinkList = []
    defeatList = []
    meltList = []
    openList = []
    weakList = []
    for object in app.levelDict:
        if 'sink' in object.effectsList:
            sinkList.append((object, object.pos))
        if 'defeat' in object.effectsList:
            defeatList.append((object, object.pos))
        if 'hot' in object.effectsList:
            meltList.append((object, object.pos))
        if 'shut' in object.effectsList:
            openList.append((object, object.pos))
        if 'weak' in object.effectsList:
            weakList.append((object, object.pos))
    sinkObjs(app, sinkList)
    defeatObjs(app, defeatList)
    meltObjs(app, meltList)
    openObjs(app, openList)
    weakObjs(app, weakList)
            
def deleteObject(app, object): #call this on sink, defeat, hot/melt, XX IS empty. 
    if object.preSink:
        prevCell = object.preSink
    else:
        prevCell = object.pos
    app.levelDict.pop(object, None)
    app.turnMoves.append((object, object.type, object.effectsList, object.attribute, prevCell))
        
def sinkObjs(app, sinkList): #sink object remove function (kills everything not FLOAT in its cell)
    sinkedObject = False
    for (sinkObject, cell) in sinkList:
        if cell and len(getObjectsInCell(app, *cell)) > 1: 
            #if theres more than one object in the cell, we delete everything in the cell
            if len(getObjectsInCell(app, *cell)) == 2:
                for object in getObjectsInCell(app, *cell):
                    if 'float' in object.effectsList:
                        return None
            for objectToSink in getObjectsInCell(app, *cell):
                if ('float' not in objectToSink.effectsList
                    or ('float' in sinkObject.effectsList and 'float' in objectToSink.effectsList)): 
                    #FLOAT objects only check each other.
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

def meltObjs(app, meltList): #melt object remove function (kills everything not FLOAT in its cell)z
    meltedObject = False
    for (hotObject, cell) in meltList:
        print(hotObject.attribute)
        if hotObject.attribute == 'level':
            for object in app.levelDict:
                if 'melt' in object.effectsList:
                    deleteObject(app, object)
                    app.turnMoves.append((object, object.type, object.effectsList, object.attribute, object.pos))
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
                    deleteObject(app, shutObject)
                    deleteObject(app, keyObject)
                    app.turnMoves.append((shutObject, shutObject.type, shutObject.effectsList, shutObject.attribute, cell))
                    openedObject = True
                    break
    if openedObject:
        playRandomOpenSound()
        
def weakObjs(app, weakList): #weak object remove function
    killedObject = False
    for (weakObject, cell) in weakList:
        if cell and len(getObjectsInCell(app, *cell)) > 1:
            deleteObject(app, weakObject)
            killedObject = True
            app.turnMoves.append((weakObject, weakObject.type, weakObject.effectsList, weakObject.attribute, cell))
    if killedObject:  
        playRandomDefeatSound()

#reset functions--------------------------------
def resetLevel(app):
    app.levelDict = copy.deepcopy(app.level.dict)
    
    #define game states
    app.noPlayer = False
    app.levelWin = False
    app.askReset = False
    app.paused = False
    
    #initialize level
    #make move history and turnMove sets, then get all rules from the board and define players
    app.moveHistory = []
    app.turnMoves = []
    app.levelRules = compileRules(app)
    app.checkSoundList = []
    app.objects = getAllObjects(app)
    app.players = getPlayer(app)
    refresh(app)
    
#refresh function here for global access to everything
def refresh(app):
    #rule refresh   
    refreshRules(app)
    swapObjs(app)
    autoMoveObjs(app)
    deleteBoard(app)
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
        operator, ruleTuple = tuple
        if operator == 'power':
            for objectToPower in ruleTuple:
                returnList.append(objectToPower)
            continue
        else: 
            (itemWord, effectWord) = ruleTuple
            if operator == 'is':
                continue
            elif operator.attribute == 'and': #this ensures the 'AND' statement is looked at last
                #so game can accurately grab powered state of the words around it. 
                returnList.insert(-2, operator)
            else:
                returnList.insert(0, operator)
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
        