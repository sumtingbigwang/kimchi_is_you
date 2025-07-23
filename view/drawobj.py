import sys
sys.path.insert(0, '/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/model')
from cmu_graphics import *
from model.objects import *

def getCellLeftTop(app, row, col):
    cellLeft = app.boardLeft + col * app.cellSize
    cellTop = app.boardTop + row * app.cellSize
    return (cellLeft, cellTop)

def getCellSize(app):
    return (app.cellSize, app.cellSize)

def drawGame(app,levelDict):
    for item in levelDict:
        if isinstance(item, str) and item == 'size':
            continue
        elif isinstance(item, obj): #draw objects
            name = item.name
            dir = item.dir
            color = item.color
            labelcolor = item.labelcolor
            if levelDict[item] == None:
                pass 
            else:
                for instance in levelDict[item]:
                    instance = instance[::-1] #convert x-y data to row/col, inefficient, fix later
                    drawObject(app,*instance,dir,name,color,labelcolor)
                
        elif isinstance(item, subj) or isinstance(item, eq) or isinstance(item, effect):
            #draw words
            if isinstance(item, eq):
                name = 'IS'
            elif isinstance(item, effect):
                name = item.desc
            else:
                name = item.obj.name
            color = item.color
            powered = item.powered
            for instance in levelDict[item]:
                instance = instance[::-1] #convert x-y data to row/col, inefficient, fix later
                drawWord(app,*instance, name, color, powered)

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