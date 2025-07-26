from ast import Index
from cmu_graphics import *
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
    app.spriteSheet = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/spritesheet.png')
    app.objectSheet = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/objectsheet.png')
    app.wordSheet = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/wordsheet.png')
    app.wallSheet = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/wallsheet.png')
    app.objectSheet2 = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/objectsheet2.png')

def loadSprites(app):
    spriteDict = dict()
    for obj in app.levelDict:
        spriteDict[obj.attribute] = dict() 
        if obj.drawInfo.type == 'sprite': #draw the sprites 
             #get the direction dictionary, whose values are column coordinates in the spritesheet
             #which initSprites uses to create a list of frames. 
             #initialize a dictionary for the direction animations. 
            for direction in obj.drawInfo.spriteList: #go through each direction
                spriteDict[obj.attribute][direction] = initSprites(app.spriteSheet, obj.drawInfo.spriteList[direction])
                
        elif obj.drawInfo.type == 'spriteWord':
            for state in obj.drawInfo.spriteList:
                spriteDict[obj.attribute][state] = initWordSprites(app.spriteSheet, obj.drawInfo.spriteList[state])
        
        elif obj.drawInfo.type == 'objectWord':
            for state in obj.drawInfo.spriteList:
                spriteDict[obj.attribute][state] = initWordSprites(app.objectSheet, obj.drawInfo.spriteList[state])
        
        elif obj.drawInfo.type == 'wallWord':
            for state in obj.drawInfo.spriteList:
                spriteDict[obj.attribute][state] = initWordSprites(app.wallSheet, obj.drawInfo.spriteList[state])
        
        elif obj.drawInfo.type == 'wall':
            for index in obj.drawInfo.spriteList:
                spriteDict[obj.attribute][index] = initWallSprites(app.wallSheet, obj.drawInfo.spriteList[index])
        
        elif obj.drawInfo.type == 'word':
            for state in obj.drawInfo.spriteList:
                spriteDict[obj.attribute][state] = initWordSprites(app.wordSheet, obj.drawInfo.spriteList[state])
                
        elif obj.drawInfo.type == 'object':
            spriteDict[obj.attribute] = initObjectSprites(app.objectSheet, obj.drawInfo.spriteList)

    return spriteDict #return dictionary

#okay, confusing as fuck. But it goes:
# spriteDict = {
#     'BABA': {
#         'right': {
#             'legs in': [frame1, frame2, frame3],
#             'standing': [frame1, frame2, frame3],
#             'legs out': [frame1, frame2, frame3]
#         }
#         'left:{}....
#and so on and so forth. So, when we want to play the animation, we do:
# spriteDict[obj.name][app.direction]
# [state (updates with repeated key presses)][app.animIndex (updates automatically)] 

def cropCompile(topx, topy, sheet, stack):
    for i in range(3):
        frame = sheet.crop((topx, topy + 25*i, topx+23, topy+25*(i+1)-1))
        frame = removeBackground(frame)
        stack.append(CMUImage(frame))

def initSprites(spriteSheet,spriteCoords): 
    spriteImages = []
    for state in spriteCoords:
        stateImages = []
        topx, topy = state
        cropCompile(topx, topy, spriteSheet, stateImages)
        spriteImages.append(stateImages)   
    return spriteImages

def initWordSprites(spriteSheet, spriteCoords):
    spriteImages = []
    for coord in spriteCoords:
        cropCompile(coord[0], coord[1], spriteSheet, spriteImages)
    return spriteImages
                
def initObjectSprites(objectSheet, objectCoord):
    spriteImages = []
    x,y = objectCoord
    cropCompile(x,y, objectSheet, spriteImages)
    return spriteImages

def initWallSprites(wallSheet, wallCoords):
    spriteImages = []
    cropCompile(wallCoords[0], wallCoords[1], wallSheet, spriteImages)
    return spriteImages

def removeBackground(image):
    image = image.convert('RGBA')
    for i in range(image.width):
      for j in range(image.height):
        pixel = image.getpixel((i, j))  
        if ((pixel[0] == 84 and pixel[1] == 165 and pixel[2] == 75)
            or (pixel[0] == 70 and pixel[1] == 152 and pixel[2] == 59)): #green screen
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
def fuckThisShit(sheet, spriteCoords):
    for coord in spriteCoords:
        for i in range(3):
            topx, topy = coord
            image = sheet.crop((topx, topy + 25*i, topx+23, topy+25*(i+1)-1))
            image = image.convert('RGBA')
            for i in range(image.width):
                for j in range(image.height):
                    pixel = image.getpixel((i, j))
                    print(pixel)