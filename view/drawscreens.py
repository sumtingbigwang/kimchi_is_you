import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *
from view.drawinfo import *
from view.drawobj import *
from model.lookup import getPlayer

# draw win / 'lose' / reset level screens --------------------------------------
def drawMapScreen(app,color):
    cellWidth, cellHeight = getCellSize(app)
    width = 11*cellWidth
    height = cellHeight
    drawImage(CMUImage(Image.open(f'view/menusprites/newmap.png')), *getCellLeftTop(app, 0, 0), 
              width=app.cellWidth * app.cols, height=app.cellHeight * app.rows)
    
    #MAP level name label here, convert to fString
    drawLabel('MAP', *getCellLeftTop(app, -0.7, 1),
              size = app.cellHeight,
              fill = 'white', bold = True, font = 'babafont', align = 'center')
    
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
        'Press Z to undo',
        app.width*0.25,
        app.height*0.075,
        fill='white', #white is a placeholder color. 
        size= app.cellHeight,
        bold= True,
        align='center'
    )
    drawLabel(
        'Press R to reset',
        app.width*0.75,
        app.height*0.075,
        fill='white', #white is a placeholder color. 
        size= app.cellHeight,
        bold= True,
        align='center'
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
    #(2, 0): resume
    resumeCoords = getCellLeftTop(app, 0, buttonRow)
    resumeImage = CMUImage(Image.open('view/pausesprites/resume.png'))
    drawImage(resumeImage, *resumeCoords, width=width*cellWidth, height=height*cellHeight)
    
    
    #(2, 4): restart
    restartCoords = getCellLeftTop(app, 1, buttonRow)
    restartImage = CMUImage(Image.open('view/pausesprites/restart.png'))
    drawImage(restartImage, *restartCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 6): settings
    settingsCoords = getCellLeftTop(app, 2, buttonRow)
    settingsImage = CMUImage(Image.open('view/pausesprites/settings.png'))
    drawImage(settingsImage, *settingsCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 6): return to map
    mapCoords = getCellLeftTop(app, 3, buttonRow)
    mapImage = CMUImage(Image.open('view/pausesprites/map.png'))
    drawImage(mapImage, *mapCoords, width=width*cellWidth, height=height*cellHeight)
    
    #(2, 8): return to menu
    menuCoords = getCellLeftTop(app, 4, buttonRow)
    menuImage = CMUImage(Image.open('view/pausesprites/menu.png'))
    drawImage(menuImage, *menuCoords, width=width*cellWidth, height=height*cellHeight)
    
    #draw pointer 
    drawSprite(app, obj('Pointer','baba'), *getCellLeftTop(app, 0+app.pointerIdx,buttonRow-1), cellWidth)

    #draw rules
    
    drawLabel(f'CURRENT RULES: {printRules(app.level.rules)}', 
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
    
    drawLabel(f'DEBUG MODE: {'ON' if app.debugMode else 'OFF'}', 
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
    
    
    
    
    # drawLabel(
    #     'Paused',
    #     app.width/2,
    #     app.height/2,
    #     fill='white', #white is a placeholder color. 
    #     size=2 * app.cellHeight,
    #     bold= True,
    #     align='center'
    # )