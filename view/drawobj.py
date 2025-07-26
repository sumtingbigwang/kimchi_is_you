import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *
from view.drawinfo import *
from model.lookup import *

def getCellLeftTop(app, row, col):
    if isinstance(row, str): #shitty fix. 
        #getCellLeftTop keeps reading row, col as the move history tuple for some reason.
        (intendedRow, intendedCol) = col
    else:
        intendedRow, intendedCol = row, col
    cellLeft = app.boardLeft + intendedCol * app.cellSize
    cellTop = app.boardTop + intendedRow * app.cellSize
    return (cellLeft, cellTop)

def getCellSize(app):
    return (app.cellSize, app.cellSize)

def drawPlayers(app, levelDict):
    players = getPlayer(app.level)
    for player in players:
        drawObject(app, player)

def drawNonPlayers(app, levelDict):
    nonPlayers = [item for item in levelDict if isinstance(item, obj) 
                   and 'you' not in item.name
                   and item.pos != None]
    for nonPlayer in nonPlayers:
        if isinstance(nonPlayer.pos[1], str):
            (position, direction) = nonPlayer.pos
            (x,y) = position
            drawObject(app, nonPlayer)
        else:
            x, y = nonPlayer.pos
            drawObject(app, nonPlayer)

def drawWords(app, levelDict):
    words = [item for item in levelDict if isinstance(item, subj) or isinstance(item, eq) or isinstance(item, effect)]
    for word in words:
        drawWord(app, word)


def drawGame(app,levelDict):
#(!!) Cursor AI: implemented module to draw players above non-player objects

    # Get all objects
    all_objects = [item for item in levelDict if isinstance(item, obj)]
    # Get player objects
    players = getPlayer(app.level)
    
    drawNonPlayers(app, levelDict)
    drawPlayers(app, levelDict)
    drawWords(app, levelDict)

def drawObject(app, obj):
    col, row = obj.pos
    cellLeft, cellTop = getCellLeftTop(app,row,col)
    cellWidth, cellHeight = getCellSize(app)
    name = obj.drawInfo.name
    color = obj.drawInfo.color
    labelcolor = obj.drawInfo.labelcolor
    spriteList = obj.drawInfo.spriteList
    dir = obj.direction
    
    if obj.drawInfo.type == 'sprite':
        drawSprite(app, obj, cellLeft, cellTop, cellWidth)
    elif obj.drawInfo.type == 'object':
        drawObj(app, obj, cellLeft, cellTop, cellWidth)
    elif obj.drawInfo.type == 'wall':
        drawWall(app, obj, cellLeft, cellTop, cellWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
        drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, 
            fill = labelcolor, size = 1.75*(cellWidth**0.5), bold = True, align = 'center')
        drawLabel(f'{dir}',cellLeft + cellWidth/2, cellTop + cellHeight/2+10, 
            fill = labelcolor, size = 1.5*(cellWidth**0.5), bold = True, align = 'center')
                
def drawWord(app, word):
    col, row = word.pos
    name = word.drawInfo.name
    color = word.drawInfo.color
    powered = word.powered
    wordType = word.drawInfo.type
    spriteList = word.drawInfo.spriteList
    cellLeft, cellTop = getCellLeftTop(app,row,col)
    cellWidth, cellHeight = getCellSize(app)
    if (wordType == 'spriteWord' 
        or wordType == 'objectWord' 
        or wordType == 'word' 
        or wordType == 'wallWord'):
        drawSpriteWord(app, word, cellLeft, cellTop, cellWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
        opacity = 100
        if not powered: #make unpowered words grey to indicate they're not in play
            opacity = 60
        #also swap this out for reading an image
        drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, opacity = opacity,
                fill = 'white', size = 2*(cellWidth**0.5), bold = True, align = 'center')
    
#we make the spriteWord distinction because it's found on another sprite sheet
#(i'm lazy)
def drawSpriteWord(app, word, cellLeft, cellTop, cellWidth): 
    state = 'powered' if word.powered else 'unpowered'
    animIndex = app.animIndex
    sprite = app.spriteDict[word.attribute][state][animIndex]
    drawImage(sprite, cellLeft, cellTop, width=cellWidth, height=cellWidth)

def drawSprite(app, obj, cellLeft, cellTop, cellWidth):
    dir = obj.direction
    state = obj.stateCount
    animIndex = app.animIndex
    sprite = app.spriteDict[obj.attribute][dir][state][animIndex]
    drawImage(sprite, cellLeft, cellTop, width=cellWidth, height=cellWidth)
    
def drawObj(app, obj, cellLeft, cellTop, cellWidth):
    animIndex = app.animIndex
    sprite = app.spriteDict[obj.attribute][animIndex]
    drawImage(sprite, cellLeft, cellTop, width=cellWidth, height=cellWidth)
    
def drawWall(app, obj, cellLeft, cellTop, cellWidth):
    animIndex = app.animIndex
    wallIndex = checkWall(app, obj)
    sprite = app.spriteDict[obj.attribute][wallIndex][animIndex]
    drawImage(sprite,cellLeft, cellTop, width=cellWidth, height=cellWidth)

#so the spritesheet for walls is organized in a very particular way. 
#i am too fucking tired to explain this but seunghyeok found some pattern
#chekc the walllocations.txt file fore more
def checkWall(app,obj):
    wallX, wallY = obj.pos
    index = 0
    dirs = [(0,1,8), (1,0,1), (0,-1,2), (-1,0,4)]
    for dir in dirs:
        dx, dy, indexAdd = dir
        newX, newY = wallX + dx, wallY + dy
        tgtObjs = getObjectsInCell(app.levelDict, newX, newY)
        for obj in tgtObjs:
            if obj.attribute == 'wall':
                print('found wall')
                index += indexAdd
    return index
        