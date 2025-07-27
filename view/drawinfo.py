from tracemalloc import start
from cmu_graphics import * 
from PIL import Image
#We want ALL OF THE SPRITE DRAW DATA HERE. E.G.
class drawInfo:
    #replace the following with sprite image links. should be (self, position1, position2, position3)
    def __init__(self, name, type, color, labelcolor, spriteList = None):
        self.name = name
        self.type = type
        self.color = color
        self.labelcolor = labelcolor
        self.spriteList = spriteList

#crop radius: 24x24
#barrier: 1 pixel 
#starts at (1,1)
#crop: corners, top left and bottom right


#ADDING A SPRITE:
#update objDrawDict/wordDrawDict in objects.pypa
#update this file with crop coordinates, name, and type
#update loadimages.py (if you need to)


#SPRITES HAVE THE FOLLOWING ANIMATION STRUCTURE:
# - Sprite: BABA, WALL, ROCK, etc. 
#      - Direction: right, up, left, down
#           - State: legs in, standing, legs out 
#                  -Frame: 0, 1, 2

#menu-related sprites--------------------------------
menuDraw = drawInfo('MENU', 'menu', 'white', 'black', None)

startDict = {'start', 'startP'}
startDraw = drawInfo('START', 'button', 'white', 'black', startDict)

continueDict = {'continue', 'continueP'}
continueDraw = drawInfo('CONTINUE', 'button', 'white', 'black', continueDict)

settingsDict = {'settings', 'settingsP'}
settingsDraw = drawInfo('SETTINGS', 'button', 'white', 'black', settingsDict)

exitDict = {'exit', 'exitP'}
exitDraw = drawInfo('EXIT', 'button', 'white', 'black', exitDict)

mapDict = {'map', 'mapP'}
mapDraw = drawInfo('MAP', 'button', 'white', 'black', mapDict)

menuPauseDict = {'pause', 'pauseP'}
menuPauseDraw = drawInfo('PAUSE', 'button', 'white', 'black', menuPauseDict)

restartDict = {'restart', 'restartP'}
restartDraw = drawInfo('RESTART', 'button', 'white', 'black', restartDict)

resumeDict = {'resume', 'resumeP'}
resumeDraw = drawInfo('RESUME', 'button', 'white', 'black', resumeDict)

settingsDict = {'settings', 'settingsP'}
settingsDraw = drawInfo('SETTINGS', 'button', 'white', 'black', settingsDict)

cursorDict = {
              'unpowered': [(376,852)],
              'powered': [(474.5,852)]
              }
cursorDraw = drawInfo('CURSOR', 'cursor', 'white', 'black', cursorDict)

#player-related sprites--------------------------------
babaDict= {
    'right': [(51+25*i+1,1) for i in range(4)],
    'up': [(151+25*i+1,1) for i in range(4)],
    'left': [(251+25*i+1,1) for i in range(4)],
    'down': [(351+25*i+1,1) for i in range(4)]
}
babaDraw = drawInfo('BABA', 'sprite', 'grey', 'white', babaDict)


babaWordDict = {
    'powered': [(26, 1)],
    'unpowered': [(1, 1)]
}
babaWordDraw = drawInfo('BABAWORD', 'spriteWord', 'grey', 'white', babaWordDict)

#object-related sprites--------------------------------
rockDict = (226,601)
rockDraw = drawInfo('ROCK', 'object', 'saddleBrown', 'white', rockDict)

rockWordDict = {
    'powered': [(201,601)],
    'unpowered': [(176,601)]
}
rockWordDraw = drawInfo('ROCKWORD', 'objectWord', 'saddleBrown', 'white',rockWordDict)


flagDict = (102,226)
flagDraw = drawInfo('FLAG', 'object', 'gold', 'white', flagDict)

flagWordDict = {
    'powered': [(77,226)],
    'unpowered': [(51,226)]
}
flagWordDraw = drawInfo('FLAGWORD', 'objectWord', 'gold', 'white', flagWordDict)

tileDict = (227,751)
tileDraw = drawInfo('TILE', 'object', 'saddleBrown', 'white', tileDict)

tileWordDict = {
    'powered': [(202,751)],
    'unpowered': [(177,751)]
}
tileWordDraw = drawInfo('TILEWORD', 'objectWord', 'saddleBrown', 'white', tileWordDict)



#wall-related sprites--------------------------------
wallDict = {i:(73+25*i+1,1501) for i in range(16)}
wallDraw = drawInfo('WALL', 'wall', 'dimGrey', 'white', wallDict)

wallWordDict = {
    'powered': [(48,1501)],
    'unpowered': [(23,1501)]
}
wallWordDraw = drawInfo('WALLWORD', 'wallWord', 'dimGrey', 'white', wallWordDict)


#object2(animated, *usually non player objects *)--------------------------------


#words--------------------------------
equalsDict = {
    'powered': [(226.5,76)],
    'unpowered': [(251.5,76)]
}
equalsDraw = drawInfo('IS', 'word', 'black', 'white', equalsDict)

hasDict = {
    'powered': [(26.5,151)],
    'unpowered': [(1.5,151)]
}
hasDraw = drawInfo('HAS', 'word', 'black', 'white', hasDict)

youDict = {
    'powered': [(276.5,226)],
    'unpowered': [(251.5,226)]
}
youDraw = drawInfo('YOU', 'word', 'grey', 'white', youDict)


pushDict = {
    'powered': [(51.5,301)],
    'unpowered': [(26.5,301)]
}
pushDraw = drawInfo('PUSH', 'word', 'saddleBrown', 'white', pushDict)

stopDict = {
    'powered': [(201.5,301)],
    'unpowered': [(176.5,301)]
}
stopDraw = drawInfo('STOP', 'word', 'dimGrey', 'white', stopDict)

winDict = {
    'powered': [(276.5,1123)],
    'unpowered': [(251.5,1123)]
}
winDraw = drawInfo('WIN', 'word', 'gold', 'white', winDict)



