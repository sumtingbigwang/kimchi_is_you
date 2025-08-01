import sys, time
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *
from model.lookup import getPlayer, getFirstObject
from view.drawinfo import *
from view.drawobj import *
from view.drawgrid import *
from view.loadimages import *
from levels import *

#draw map screen --------------------------------------------------------------

hintDict = {
    -1: "IF YOU CAN'T GET TO LEVEL 22, TRY MAKING LEVEL 21 INTO SOMETHING!",
    1: 'IF KIMCHI IS YOU AND FLAG IS WIN, WHAT DO YOU NEED TO WIN?',
    2: "IS WALL STILL 'STOP' IF YOU DON'T MAKE IT SO?",
    3: "WHAT IF WHATEVER IS 'YOU' IS ALSO 'WIN'?",
    4: "THERE'S NOT ENOUGH ROCKS TO FILL THE LAKE. BUT WHO SAYS YOU HAVE TO FILL THE LAKE?",
    5: "MAYBE ITEMS CAN INTERACT WITH WORDS?",
    6: "WHAT IF SOMETHING'S 'HOT' AND 'MELT' AT THE SAME TIME?",
    7: "WHAT OTHER OBJECT CAN BE 'YOU'?",
    8: "IS 'WALL IS STOP' IN THE RULES?",
    9: "COULD KEKE FETCH THE FLAG FOR YOU SOMEHOW?",
    10: "WHAT HAPPENS IF SOMETHING AND SOMETHING ARE 'YOU'?",
    11: "'ROCK IS ROCK' OVERRIDES 'ROCK IS FLAG'!",
    12: "DOES THE KEY HAVE TO BE 'OPEN'?",
    13: "CLEAR A PATH BY MAKING THINGS 'WEAK'!",
    14: "'IS NOT' STATEMENTS OVERRIDE 'IS' ONES!",
    15: "MAYBE YOU DON'T HAVE TO BE BABA? OR BABA DOESN'T HAVE TO TOUCH THE FLAG?",
    16: "WE CAN MAKE TWO MOVING OBJECTS, AND THOSE PIPE GAPS LOOK LIKE THEY COULD FIT SOME WORDS IN THEM...",
    17: "CAN THE BOLT HELP YOU BREAK OUT OF THE 'DEFEAT' CLAUSE?",
    18: "MAKE AN OPENING ON THE LEFT USING TWO PLAYERS. PERHAPS THE 'AND' WORD CAN HELP YOU REACH THE 'WIN' BLOCK IN THE MIDDLE...",
    19: "WHAT HAPPENS IF WE DOUBLE NEGATE A SENTENCE? LIKE NOT KEKE IS NOT HOT, NOT KIMCHI IS NOT DEFEAT... OR?",
    20: "IF KEKE ISN'T YOU, HE CAN PASS THROUGH THE ALGAE SAFELY. MAYBE SOMETHING COULD PUSH HIM OVER AND MAKE HIM 'YOU' ON THE OTHER SIDE...",
    21: "WHAT HAPPENS IF 'LEVEL' IS 'HOT', AND SOMETHING IS MELT? (THIS LEVEL IS HARD! SEARCH FOR 'FRAGILE EXISTENCE SOLUTION' IF YOU CAN'T FIND IT)",
    22: "DO WE NEED A PLAYER SPRITE TO 'WIN'?",
}
mapLevelNameDict = {
    (7,13):'STARTING OFF',
    (8,13):'WHERE DO I GO?',
    (9,13):'WHAT THE HELLY?',
    (7,12):'OUT OF REACH',
    (8,12):'STILL OUT OF REACH',
    (9,12):'VOLCANO',
    (7,11):'OFF LIMITS',
    (8,11):'GRASS YARD',
    (9,11):'HIRED HELP',
    (12,12):'ICY WATERS',
    (13,12):'CHANGELESS',
    (14,12):'BURLGARY',
    (19,12):'FRAGILITY',
    (20,12):'NOT THERE',
    (21,12):'FLOAT',
    (23,9):'REMOTE CONNECTION',
    (24,9): 'RESEARCH LAB',
    (15,2): 'TINY ISLE',
    (14,2): 'CATCH',
    (13,2): 'FURTHER FIELDS',
    (12,2): 'META',
    (2,5): 'METAMETA'
}
def drawMapScreen(app,color):
    cellWidth, cellHeight = getCellSize(app)
    width = 11*cellWidth
    height = cellHeight
    drawImage(CMUImage(Image.open(f'view/menusprites/newmap.png')), *getCellLeftTop(app, 0, 0), 
              width=app.cellWidth * app.cols, height=app.cellHeight * app.rows)
    cursor = getFirstObject(app, 'cursor')
    cursorPosition = cursor.pos
    if cursorPosition in mapLevelNameDict:
        cursor.powered = True
    else:
        cursor.powered = False
    #MAP level name label here, convert to fString
    drawLabel(f'{mapLevelNameDict[cursorPosition] if cursorPosition in mapLevelNameDict else 'MAP'}', 
              *getCellLeftTop(app, -0.7, 0),
              size = app.cellHeight,
              fill = 'white', bold = True, font = 'babafont',
              align = 'left')
    
    #lazy implementation of level numbers
    drawLevelNumbers(app)

def drawLevelNumbers(app):
    levelCoordinates = map.objDict['tile']
    i = 1
    for coordinate in levelCoordinates:
        col, row = coordinate
        x, y = getCellLeftTop(app, row, col)
        drawLabel(f'{i}', x + app.cellHeight//2, y + app.cellHeight//2,
                  size = app.cellHeight//2,
                  fill = 'white', bold = True, font = 'babafont', align = 'center')
        i += 1
    
    
# draw win / 'lose' / reset level screens --------------------------------------  
def drawWinScreen(app,color): 
    drawRect(0,0,app.width,app.height,fill=color, opacity = 40)
    drawLabel(
        'CONGRATULATIONS!',
        app.width/2,
        app.height/2,
        fill='white', #white is a placeholder color. 
        size=2 * app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    #placeholder. the real win screen is temporary, and directs users back to the map screen after ~5 secs.
    drawLabel(
        "PRESS 'C'TO CONTINUE",
        app.width/2,
        app.height/2 + 0.25*app.height,
        fill='white', #white is a placeholder color. 
        size= 0.65* app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )

def drawGameWinScreen(app):
    drawRect(0,0,app.width,app.height,fill='gold', opacity = 40)
    drawLabel(
        'CONGRATULATIONS, AND THANK YOU!',
        app.width/2,
        app.height/2,
        fill='white', #white is a placeholder color. 
        size=2 * app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    #placeholder. the real win screen is temporary, and directs users back to the map screen after ~5 secs.
    drawLabel(
        "YOU'VE COMPLETED THE GAME! IF YOU WANT, PRESS 'C' TO KEEP PLAYING. *",
        app.width/2,
        app.height/2 + 0.25*app.height,
        fill='white', #white is a placeholder color. 
        size= 0.65* app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )

def drawResetScreen(app,color): 
    #temporary. replace all of this
    drawRect(0,0,app.width,app.height,fill= rgb(21,24,31), opacity = 60)
    drawLabel(
        'ARE YOU SURE YOU WANT TO RESET THE LEVEL?',
        app.width/2,
        app.height/2 - 0.5 * app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75 * app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    drawLabel(
        'YES / Y',
        app.width/2 - 0.4*(app.width/2),
        app.height/2+0.75*app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75* app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    drawLabel(
        'NO / N',
        app.width/2 + 0.4*(app.width/2),
        app.height/2+0.75*app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75* app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    
def drawNoPlayerScreen(app,color): 
    #also temporary. replace all of this
    drawLabel(
        'Z TO UNDO',
        app.width*0.25,
        app.height*0.075,
        fill='white', #white is a placeholder color. 
        size= app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
    drawLabel(
        'R TO RESET',
        app.width*0.75,
        app.height*0.075,
        fill='white', #white is a placeholder color. 
        size= app.cellHeight,
        bold= True,
        align='center',
        font= 'babafont'
    )
def drawLevelExplosionScreen(app,color):
    drawRect(0,0,app.width,app.height,fill='black')
    
def printRules(rulesList):
    ruleString = ''
    effectString = ''
    addedRule = False
    for tuple in rulesList:
        operator, ruletuple = tuple
        if operator == 'power':
            continue
        else:
            if ruleString != '' and addedRule:
                ruleString += ', '
            subject, effect = ruletuple
            if subject and effect:
                if effect.type == 'subj':
                    effectString = effect.obj
                else:
                    effectString = effect.attribute
                ruleToAdd = f'{subject.obj.upper()} IS {effectString.upper()}'
                if ruleToAdd not in ruleString:
                    ruleString += ruleToAdd
                    addedRule = True
                    continue
                addedRule = False
                
    return ruleString

def drawPauseScreen(app,color):
    cellWidth, cellHeight = getCellSize(app)
    height = 1 + app.rows // 25
    width = 11*height
    buttonRow = (app.cols - width)//2
    drawRect(0,0,app.width,app.height,fill=rgb(21,24,31), opacity = 60)
    #level title 

    drawLabel(f'{app.level.levelName}', *getCellLeftTop(app, 0.4, app.cols//2),
              size = app.cellHeight, fill = 'white', font = 'babafont', bold = True, align = 'center')
    
    #(2, 1): resume
    resumeCoords = getCellLeftTop(app, 1, buttonRow+0.5)
    resumeImage = CMUImage(Image.open('view/pausesprites/resume.png'))
    drawImage(resumeImage, *resumeCoords, width=width*cellWidth, height=height*cellHeight)
    
    
    #(2, 2): restart
    restartCoords = getCellLeftTop(app, 2, buttonRow+0.5)
    restartImage = CMUImage(Image.open('view/pausesprites/restart.png'))
    drawImage(restartImage, *restartCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 3): settings
    settingsCoords = getCellLeftTop(app, 3, buttonRow+0.5)
    settingsImage = CMUImage(Image.open('view/pausesprites/settings.png'))
    drawImage(settingsImage, *settingsCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 4): return to map
    mapCoords = getCellLeftTop(app, 4, buttonRow+0.5)
    mapImage = CMUImage(Image.open('view/pausesprites/map.png'))
    drawImage(mapImage, *mapCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 5): return to menu
    menuCoords = getCellLeftTop(app, 5, buttonRow+0.5)
    menuImage = CMUImage(Image.open('view/pausesprites/menu.png'))
    drawImage(menuImage, *menuCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2,6): hint
    menuCoords = getCellLeftTop(app, 6, buttonRow+0.5)
    hintImage = CMUImage(Image.open('view/pausesprites/hintP.png'))
    drawImage(hintImage, *menuCoords, width=width*cellWidth, height=height*cellHeight)
    
    #draw pointer 
    drawSprite(app, obj('Pointer','kimchi',None,'right'), *getCellLeftTop(app, 1+app.pointerIdx,buttonRow-0.5), cellWidth)

    #draw rules
    
    drawLabel(f'CURRENT RULES: {printRules(app.levelRules)}', 
              app.width//2, app.height- 1*app.cellHeight,
              size = 0.4*app.cellHeight, 
              fill = 'white', bold = True, font= 'babafont', align = 'center')
    if app.giveHint: 
        drawLabel(f'{hintDict[app.levelNum]}', 
              app.width//2, app.height- 0.5*app.cellHeight,
              size = 0.4*app.cellHeight, 
              fill = 'white', bold = True, font= 'babafont', align = 'center')
       
    
def drawSettingsScreen(app):
    cellWidth, cellHeight = getCellSize(app)
    drawRect(0,0,app.width,app.height,fill=rgb(21,24,31), opacity = 100)
    drawLabel('SETTINGS', 
            app.width//2, cellHeight,
            size = cellHeight, 
            fill = 'white', bold = True, font = 'babafont', align = 'center')
    
    drawLabel(f'DEBUG MODE (G): {'ON' if app.debugMode else 'OFF'}', 
              app.width//2, 4*cellHeight,
              size = 0.6*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    
    drawLabel(f'CURRENT MOVES PER SECOND: {pythonRound(0.6/app.latency,1)}', 
              app.width//2, 6*cellHeight,
              size = 0.6*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel('(UP/DOWN ARROWS TO CHANGE, DEFAULT 6)', 
              app.width//2, 7*cellHeight,
              size = 0.4*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel('RESET WINDOW SIZE (W)', 
              app.width//2, 9*cellHeight,
              size = 0.6*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel('(SCREEN ADJUSTS TO YOUR WINDOW SIZE!)', 
              app.width//2, 10*cellHeight,
              size = 0.4*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel("**FEATURE RECOMMENDED IN WINDOWED MODE ONLY. PLAY THE GAME IN FULLSCREEN FOR BEST EXPERIENCE.", 
              app.width//2, 10.5*cellHeight,
              size = 0.2*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel('ESC TO RETURN', 
              app.width//2, app.height - 2*cellHeight,
              size = cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    
    
def startup(app):
    print('\n\n\n\n\n')
    print('--------------------------------')
    print('Levels Loaded! Ready to Go!')
    
    # drawLabel(
    #     'Paused',
    #     app.width/2,
    #     app.height/2,
    #     fill='white', #white is a placeholder color. 
    #     size=2 * app.cellHeight,
    #     bold= True,
    #     align='center'
    # )