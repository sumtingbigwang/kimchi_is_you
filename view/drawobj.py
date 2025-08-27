import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'model'))
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

def drawPlayers(app):
    players = getPlayer(app)
    for player in players:
        drawObject(app, player)

def drawNonPlayers(app):
    nonPlayers = [item for item in app.levelDict if isinstance(item, obj) 
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

def drawWords(app):
    words = [item for item in app.levelDict if isinstance(item, subj) or isinstance(item, eq) or isinstance(item, effect)]
    for word in words:
        drawWord(app, word)


def drawGame(app):
    drawRect(0,0,app.width,app.height,fill=app.level.background) 
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight, fill = app.level.cellColor)
    drawNonPlayers(app)
    drawPlayers(app)
    drawWords(app)

def drawObject(app, obj):
    col, row = obj.pos
    cellLeft, cellTop = getCellLeftTop(app,row,col)
    cellWidth, cellHeight = getCellSize(app)
    name = obj.drawInfo.name
    color = obj.drawInfo.color
    labelcolor = obj.drawInfo.labelcolor
    spriteList = obj.drawInfo.spriteList
    dir = obj.direction
    match obj.drawInfo.type:
        case 'sprite' | 'object2':
            drawSprite(app, obj, cellLeft, cellTop, cellWidth)
        case 'object':
            drawObj(app, obj, cellLeft, cellTop, cellWidth)
        case 'wall':
            drawWall(app, obj, cellLeft, cellTop, cellWidth)
        case 'menu':
            drawMenu(app, obj, cellLeft, cellTop, cellWidth)
        case 'cursor':
            drawCursor(app, obj, cellLeft, cellTop, cellWidth)
        case _:
            drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
            drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, 
                fill = labelcolor, size = 1.75*(cellWidth**0.5), bold = True, align = 'center')
                
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
        or wordType == 'wallWord'
        or wordType == 'object2Word'):
        drawSpriteWord(app, word, cellLeft, cellTop, cellWidth)
    elif wordType == 'button':
        drawButton(app, word, cellLeft, cellTop, cellWidth)
    else:
        drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)
        opacity = 100
        if not powered: #make unpowered words grey to indicate they're not in play
            opacity = 60
        #also swap this out for reading an image
        drawLabel(f'{name}',cellLeft + cellWidth/2, cellTop + cellHeight/2, opacity = opacity,
                fill = 'white', size = 2*(cellWidth**0.5), bold = True, align = 'center')
    
#menu draw stuff--------------------------------

def drawButton(app, obj, cellLeft, cellTop, cellWidth):
    state = 1 if obj.powered else 0
    animIndex = app.animIndex
    sprite = app.spriteDict[obj.attribute][state]
    drawImage(sprite, cellLeft, cellTop, width=7*cellWidth, height=cellWidth)
    
def drawMenu(app, obj, cellLeft, cellTop, cellWidth):
    cellWidth, cellHeight = getCellSize(app)
    color = obj.drawInfo.color
    labelcolor = obj.drawInfo.labelcolor
    name = obj.drawInfo.name
    width = 13*cellWidth
    height = 4*cellHeight
    drawImage(app.spriteDict['title'][app.animIndex], cellLeft, cellTop, width=width, height=height)
    
def drawCursor(app, obj, cellLeft, cellTop, cellWidth):
    state = 'powered' if obj.powered else 'unpowered'
    animIndex = app.animIndex
    sprite = app.spriteDict[obj.attribute][state][animIndex]
    drawImage(sprite, cellLeft, cellTop, width=cellWidth, height=cellWidth)

#sprite draw stuff--------------------------------
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
    if obj.attribute == 'kosbie':
        drawImage(CMUImage(Image.open('code/view/spritesheets/kosbie.png')), 
                  cellLeft, cellTop, width=cellWidth, height=cellWidth)
    elif obj.drawInfo.type == 'object2':
        sprite = app.spriteDict[obj.attribute][dir][0][animIndex]
        drawImage(sprite, cellLeft, cellTop, width=cellWidth, height=cellWidth)
    else:
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
#wall segments (e.g. corner connectors, vertical connectors, horizontal ends) are ordered in terms of the origin wall
#and the number / position of walls next to it.
#if a wall is alone, it has index 0 (lone wall image comes first)
#if a wall has a single wall to the right of it, it has index 1, and so on.
#now, if you have a wall above and to the right of you, you have index 1+8 = 9.
#this turns out to be the index of the bottom-left connector segment!
def checkWall(app,obj):
    wallX, wallY = obj.pos
    index = 0
    wallIn = False
    overlapObjs = getObjectsInCell(app, wallX, wallY)
    
    for obj in overlapObjs: #shitty check for overlap
        if obj.drawInfo.type == 'wall' and wallIn:
            return 0
        elif not wallIn and obj.drawInfo.type == 'wall':
            wallIn = True
            
    dirs = [(0,1,8), (1,0,1), (0,-1,2), (-1,0,4)]
    for dir in dirs: #check all 4 directions for walls
        dx, dy, indexAdd = dir
        newX, newY = wallX + dx, wallY + dy
        tgtObjs = getObjectsInCell(app, newX, newY)
        for targetObject in tgtObjs:
            if (targetObject.drawInfo.type == 'wall'
                and targetObject.attribute == obj.attribute): #found a wall, add the index of the wall segment
                index += indexAdd
    return index % 16
        