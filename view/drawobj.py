import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *
from view.drawinfo import *
from model.lookup import getPlayer

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellSize
    cellTop = app.boardTop + row * app.cellSize
    return (cellLeft, cellTop)

def getCellSize(app):
    return (app.cellSize, app.cellSize)

def drawPlayers(app, levelDict):
    players = getPlayer(app.level)
    for player in players:
        drawObject(app, player.pos[1], player.pos[0], 
                   player.direction, player.drawInfo.name, 
                   player.drawInfo.color, player.drawInfo.labelcolor)

def drawNonPlayers(app, levelDict):
    non_players = [item for item in levelDict if isinstance(item, obj) 
                   and 'you' not in item.name
                   and item.pos != None]
    for non_player in non_players:
        drawObject(app, non_player.pos[1], non_player.pos[0], 
                   non_player.direction, non_player.drawInfo.name, 
                   non_player.drawInfo.color, non_player.drawInfo.labelcolor)

def drawWords(app, levelDict):
    words = [item for item in levelDict if isinstance(item, subj) or isinstance(item, eq) or isinstance(item, effect)]
    for word in words:
        drawWord(app, word.pos[1], word.pos[0], word.drawInfo.name, word.drawInfo.color, word.powered)

def drawGame(app,levelDict):
#(!!) Cursor AI: implemented module to draw players above non-player objects

    # Get all objects
    all_objects = [item for item in levelDict if isinstance(item, obj)]
    # Get player objects
    players = getPlayer(app.level)
    
    drawNonPlayers(app, levelDict)
    drawPlayers(app, levelDict)
    drawWords(app, levelDict)

def drawObject(app, row, col, dir,name,color,labelcolor): 
    cellLeft, cellTop = getCellLeftTop(app,row,col)
    cellWidth, cellHeight = getCellSize(app)
    #swap this out for reading an image
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
    drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, 
            fill = labelcolor, size = 1.75*(cellWidth**0.5), bold = True, align = 'center')
    drawLabel(f'{dir}',cellLeft + cellWidth/2, cellTop + cellHeight/2+10, 
            fill = labelcolor, size = 1.5*(cellWidth**0.5), bold = True, align = 'center')

def drawWord(app, row, col, name, color, powered):
    cellLeft, cellTop = getCellLeftTop(app,row,col)
    cellWidth, cellHeight = getCellSize(app)
    opacity = 100
    if not powered: #make unpowered words grey to indicate they're not in play
        opacity = 60
        
    #also swap this out for reading an image
    drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, opacity = opacity,
              fill = color, size = 2*(cellWidth**0.5), bold = True, align = 'center')