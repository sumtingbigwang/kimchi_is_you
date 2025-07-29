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
mapLevelNameDict = {
    (7,13):'STARTING OFF',
    (8,13):'WHERE DO I GO?',
    (9,13):'WHAT THE HELLY?',
    (7,12):'OUT OF REACH',
    (8,12):'STILL OUT OF REACH',
    (9,12):'[LEVELNAME]',
    (7,11):'[LEVELNAME]',
    (8,11):'[LEVELNAME]',
    (9,11):'[LEVELNAME]'
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
    #temporary. replace all of this
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

def printRules(rulesList):
    ruleString = ''
    effectString = ''
    for tuple in rulesList:
        if ruleString != '':
            ruleString += ', '
        equalsObject, ruletuple = tuple
        subject, effect = ruletuple
        if effect.type == 'subj':
            effectString = effect.obj
        else:
            effectString = effect.attribute
        if len(ruleString) > 4: 
            ruleString += '\n'
        ruleString += f'{subject.obj.upper()} IS {effectString.upper()}'
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
    
    #(2, 0): resume
    resumeCoords = getCellLeftTop(app, 1, buttonRow+0.5)
    resumeImage = CMUImage(Image.open('view/pausesprites/resume.png'))
    drawImage(resumeImage, *resumeCoords, width=width*cellWidth, height=height*cellHeight)
    
    
    #(2, 4): restart
    restartCoords = getCellLeftTop(app, 2, buttonRow+0.5)
    restartImage = CMUImage(Image.open('view/pausesprites/restart.png'))
    drawImage(restartImage, *restartCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 6): settings
    settingsCoords = getCellLeftTop(app, 3, buttonRow+0.5)
    settingsImage = CMUImage(Image.open('view/pausesprites/settings.png'))
    drawImage(settingsImage, *settingsCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 6): return to map
    mapCoords = getCellLeftTop(app, 4, buttonRow+0.5)
    mapImage = CMUImage(Image.open('view/pausesprites/map.png'))
    drawImage(mapImage, *mapCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 8): return to menu
    menuCoords = getCellLeftTop(app, 5, buttonRow+0.5)
    menuImage = CMUImage(Image.open('view/pausesprites/menu.png'))
    drawImage(menuImage, *menuCoords, width=width*cellWidth, height=height*cellHeight)
    
    #draw pointer 
    drawSprite(app, obj('Pointer','kimchi'), *getCellLeftTop(app, 1+app.pointerIdx,buttonRow-0.5), cellWidth)

    #draw rules
    
    drawLabel(f'CURRENT RULES: {printRules(app.levelRules)}', 
              app.width//2,app.height- 2*app.cellHeight,
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
    
    drawLabel(f'CURRENT FPS: {pythonRound(app.stepsPerSecond,3)}', 
              app.width//2, 6*cellHeight,
              size = 0.6*cellHeight, 
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    drawLabel('(UP/DOWN ARROWS TO CHANGE, DEFAULT 5.5)', 
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