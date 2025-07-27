from ast import Index
from cmu_graphics import *
from cmu_graphics.shape_logic import t
from drawinfo import *
from model.rules import *
from model.objects import *
from drawobj import *
from urllib.request import urlopen
from PIL import Image

#crop radius: 24x24
#barrier: 1 pixel 
#starts at (1,1)
#crop: corners, top left and bottom right
#have a 2D list of images, each row is up/right/left/right animation 

#SPRITES HAVE THE FOLLOWING ANIMATION STRUCTURE:
# - Sprite: BABA, WALL, ROCK, etc. 
#      - Direction: right, up, left, down
#           - State: legs in, standing, legs out 
#                  -Frame: 0, 1, 2


#load spritesheet for cropping

def loadSheets(app):
    app.spriteSheet = Image.open('view/spritesheets/spritesheet.png')
    app.objectSheet = Image.open('view/spritesheets/objectsheet.png')
    app.wordSheet = Image.open('view/spritesheets/wordsheet.png')
    app.wallSheet = Image.open('view/spritesheets/wallsheet.png')
    app.objectSheet2 = Image.open('view/spritesheets/objectsheet2.png')
    

def loadSprites(app):
    spriteDict = dict()
    
#if obj.drawInfo.type == 'sprite': #draw the sprites 
#for direction in obj.drawInfo.spriteList: #go through each direction
#spriteDict[obj.attribute][direction] = initSprites(app.spriteSheet, obj.drawInfo.spriteList[direction])
#get the direction dictionary, whose values are column coordinates in the spritesheet
#which initSprites uses to create a list of frames. 

    #pre-load all known objects from drawinfo
    for objName, drawInfo in objDrawDict.items():
        spriteDict[objName] = dict()
        match drawInfo.type:
            case 'sprite':
                for direction in drawInfo.spriteList:
                    spriteDict[objName][direction] = initSprites(app.spriteSheet, drawInfo.spriteList[direction])
            case 'object':
                spriteDict[objName] = initObjectSprites(app.objectSheet, drawInfo.spriteList)
            case 'wall':
                for index in drawInfo.spriteList:
                    spriteDict[objName][index] = initObjectSprites(app.wallSheet, drawInfo.spriteList[index])
            case 'cursor':
                for state in drawInfo.spriteList:
                    spriteDict[objName][state] = initCursor(app.objectSheet, drawInfo.spriteList[state])
    
    #pre-load all known words from drawinfo
    for wordName, drawInfo in wordDrawDict.items():
        spriteDict[wordName] = dict()
        match drawInfo.type:
            case 'spriteWord':
                for state in drawInfo.spriteList:
                    spriteDict[wordName][state] = initWordSprites(app.spriteSheet, drawInfo.spriteList[state])
            case 'objectWord':
                for state in drawInfo.spriteList:
                    spriteDict[wordName][state] = initWordSprites(app.objectSheet, drawInfo.spriteList[state])
            case 'wallWord':
                for state in drawInfo.spriteList:
                    spriteDict[wordName][state] = initWordSprites(app.wallSheet, drawInfo.spriteList[state])
            case 'word':
                for state in drawInfo.spriteList:
                    spriteDict[wordName][state] = initWordSprites(app.wordSheet, drawInfo.spriteList[state])
            case _:
                pass
    spriteDict['title'] = loadTitle(app)
    spriteDict.update(loadButtonImages(app))
    return spriteDict
#okay, confusing as fuck. But it goes:
# spriteDict = {
#     'BABA': {
#         'right': {
#             'legs in': [frame1, frame2, frame3],
#             'standing': [frame1, frame2, frame3],
#             'legs out': [frame1, frame2, frame3]
#         }
#         'left':{}....
#and so on and so forth. So, when we want to play the animation, we access:
# spriteDict[obj.name][app.direction][state(updates with repeated key presses)][app.animIndex(updates automatically)] 

def loadTitle(app):
    titleImages = []
    for i in range(3):
        titleImages.append(CMUImage(Image.open(f'/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/menusprites/title{i+1}.png')))
    return titleImages

def loadButtonImages(app):
    buttonImages = {'continue':[],
                    'start':[],
                    'settings':[],
                    'exit':[]}
    for button in buttonImages:
        buttonImages[button] += [CMUImage(Image.open(f'view/menusprites/{button}.png'))]
        buttonImages[button] += [CMUImage(Image.open(f'view/menusprites/{button}P.png'))]
    return buttonImages

def cropCompile(topx, topy, sheet, stack): #cuz it crops and compiles. get it? fml
    for i in range(3):
        frame = sheet.crop((topx, topy + 25*i, topx+23, topy+25*(i+1)-1))
        frame = removeBackground(frame)
        stack.append(CMUImage(frame))

def initSprites(spriteSheet,spriteCoords): #this is players
    spriteImages = []
    for state in spriteCoords:
        stateImages = []
        topx, topy = state
        cropCompile(topx, topy, spriteSheet, stateImages)
        spriteImages.append(stateImages)   
    return spriteImages

def initCursor(objectSheet, cursorCoords):
    cursorImages = []
    for coord in cursorCoords:
        for i in range(3):
            topx, topy = coord
            frame = objectSheet.crop((topx + 33*i, topy, topx+33*(i+1), topy+30))
            frame = removeBackground(frame)
            cursorImages.append(CMUImage(frame))
    return cursorImages

def initWordSprites(spriteSheet, spriteCoords):
    spriteImages = []
    for coord in spriteCoords:
        cropCompile(coord[0], coord[1], spriteSheet, spriteImages)
    return spriteImages
                
def initObjectSprites(objectSheet, objectCoord):
    spriteImages = []
    cropCompile(*objectCoord, objectSheet, spriteImages)
    return spriteImages

def removeBackground(image):
    image = image.convert('RGBA')
    for i in range(image.width):
      for j in range(image.height):
        pixel = image.getpixel((i, j))  
        if ((pixel[0] == 84 and pixel[1] == 165 and pixel[2] == 75)
            or (pixel[0] == 0 and pixel[1] == 0 and pixel[2] == 0)
            or (pixel[0] == 70 and pixel[1] == 152 and pixel[2] == 59) #green screen
            or (pixel[0] == 45 and pixel[1] == 88 and pixel[2] == 148)): #get rid of blue spritesheet border
            image.putpixel((i, j), (0, 0, 0, 0))
        else: 
            r,g,b,a = pixel
            image.putpixel((i, j), (r,g,b, 255))
    return image

#this is a RGB check for a draw class.
#it has this name because it is 12:22 AM in the morning.
#and life sucks.
#and I just spent 30 minute strying to figure out what pillow is looking at,
#because the green it's seeing certainly isn't the one I'm seeing.
def pixelPicker(sheet, spriteCoords):
    for coord in spriteCoords:
        for i in range(3):
            topx, topy = coord
            image = sheet.crop((topx, topy + 25*i, topx+23, topy+25*(i+1)-1))
            image = image.convert('RGBA')
            for i in range(image.width):
                for j in range(image.height):
                    pixel = image.getpixel((i, j))
                    print(pixel)