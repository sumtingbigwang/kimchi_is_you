import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *
from view.drawinfo import *
from model.lookup import getPlayer

# draw win / 'lose' / reset level screens --------------------------------------
def drawWinScreen(app,color): 
    #temporary. replace all of this
    drawRect(0,0,app.width,app.height,fill=color, opacity = 40)
    drawLabel(
        'Congratulations!',
        app.width/2,
        app.height/2,
        fill='white', #white is a placeholder color. 
        size=2 * app.cellHeight,
        bold= True,
        align='center'
    )
    #placeholder. the real win screen is temporary, and directs users back to the map screen after ~5 secs.
    drawLabel(
        "Press 'C' to continue",
        app.width/2,
        app.height/2 + 0.25*app.height,
        fill='white', #white is a placeholder color. 
        size= 0.65* app.cellHeight,
        bold= True,
        align='center' )

def drawResetScreen(app,color): 
    #temporary. replace all of this
    drawRect(0,0,app.width,app.height,fill=color, opacity = 40)
    drawLabel(
        'Are you sure you want to reset the level?',
        app.width/2,
        app.height/2 - 0.5 * app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75 * app.cellHeight,
        bold= True,
        align='center'
    )
    drawLabel(
        'Yes / Y',
        app.width/2 - 0.4*(app.width/2),
        app.height/2+0.75*app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75* app.cellHeight,
        bold= True,
        align='center'
    )
    drawLabel(
        'No / N',
        app.width/2 + 0.4*(app.width/2),
        app.height/2+0.75*app.cellHeight,
        fill='white', #white is a placeholder color. 
        size= 0.75* app.cellHeight,
        bold= True,
        align='center'
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
    for tuple in rulesList:
        if ruleString != '':
            ruleString += ', '
        equalsObject, ruletuple = tuple
        subject, effect = ruletuple
        ruleString += f'{subject.obj.upper()} IS {effect.attribute.upper()}'
    return ruleString