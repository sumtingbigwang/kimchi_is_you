from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

#crop radius: 24x24
#barrier: 1 pixel 
#starts at (1,1)
#crop: corners, top left and bottom right
#have a 2D list of images, each row is up/right/left/right animation 


#load spritesheet for cropping
spriteSheet = Image.open('/Users/wangcomputer/Developer/School/15112/kimchi_is_you/code/view/spritesheet.png')

babaLeft = [(51+25*i+1,1) for i in range(4)]
babaUp = [(151+25*i+1,1) for i in range(4)]
babaRight = [(251+25*i+1,1) for i in range(4)]
babaDown = [(351+25*i+1,1) for i in range(4)]

#initialize sprites
def initSprites(spriteSheet,spriteCoords): 
    topx, topy = spriteCoords
    spritePilImages = []
    for i in range(3):
        spriteImage = spriteSheet.crop((topx, topy + 25*i, topx+23, topy+25*(i+1)-1))
        spritePilImages.append(spriteImage)
    return spritePilImages

#testing function
def onAppStart(app):
    app.spriteList= babaLeft
    app.spriteIdx = 0
    spritePilImages = initSprites(spriteSheet, app.spriteList[app.spriteIdx])
    app.spriteCmuImages = [CMUImage(pilImage) for pilImage in spritePilImages]
    app.spriteIndex = 0
    app.stepsPerSecond = 6
    
def onStep(app):
    app.spriteIndex = (app.spriteIndex + 1) % len(app.spriteCmuImages)

def onKeyPress(app, key):
    if key == 'up':
        app.spriteList = babaUp
    elif key == 'right':
        app.spriteList = babaRight
    elif key == 'down':
        app.spriteList = babaDown
    elif key == 'left':
        app.spriteList = babaLeft
    app.spriteIdx = (app.spriteIdx+1)%4
    spritePilImages = initSprites(spriteSheet, app.spriteList[app.spriteIdx])
    app.spriteCmuImages = [CMUImage(pilImage) for pilImage in spritePilImages]

def redrawAll(app):
    drawLabel('Sprite Demo', 400, 40, size=16)
    drawLabel('Press up/down to go faster/slower', 400, 80, size=16)
    drawLabel(f'position = {app.spriteList[app.spriteIdx]}', 400, 120, size=32)
    drawImage(app.spriteCmuImages[app.spriteIndex], 400, 400, align='center')

def main():
    runApp()

main()