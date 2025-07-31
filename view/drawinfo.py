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


#DISCLAIMER: Cursor.AI was able to help me type out ~half of the dictionaries below, provided I found and revised the coordinates.
#It took manually typing out about 25-30 of these for the bot to get the hang of generating dictionaries. 

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

kimchiDict = {
    'right': [(602+25*i,226) for i in range(4)],
    'up': [(702+25*i,226) for i in range(4)],
    'left': [(802+25*i,226) for i in range(4)],
    'down': [(902+25*i,226) for i in range(4)]
}
kimchiDraw = drawInfo('KIMCHI', 'sprite', 'saddleBrown', 'white', kimchiDict)


kimchiWordDict = {
    'powered': [(577,226)],
    'unpowered': [(552,226)]
}
kimchiWordDraw = drawInfo('KIMCHIWORD', 'spriteWord', 'saddleBrown', 'white', kimchiWordDict)

kosbieDict = {}
kosbieDraw = drawInfo('KOSBIE', 'sprite', 'saddleBrown', 'white', kosbieDict)

kosbieWordDict = {
    'powered': [(577,301)],
    'unpowered': [(552,301)]
}
kosbieWordDraw = drawInfo('KOSBIEWORD', 'spriteWord', 'saddleBrown', 'white', kosbieWordDict)

kekeDict = {
    'right': [(52+25*i,601) for i in range(4)],
    'up': [(152+25*i,601) for i in range(4)],
    'left': [(252+25*i,601) for i in range(4)],
    'down': [(352+25*i,601) for i in range(4)]
}
kekeDraw = drawInfo('KEKE', 'sprite', 'saddleBrown', 'white', kekeDict)

kekeWordDict = {
    'powered': [(27,601)],
    'unpowered': [(2,601)]
}
kekeWordDraw = drawInfo('KEKEWORD', 'spriteWord', 'saddleBrown', 'white', kekeWordDict)

jijiDict = {
    'right': [(52+25*i,526) for i in range(4)],
    'up': [(152+25*i,526) for i in range(4)],
    'left': [(252+25*i,526) for i in range(4)],
    'down': [(352+25*i,526) for i in range(4)]
}
jijiDraw = drawInfo('JIJI', 'sprite', 'saddleBrown', 'white', jijiDict)

jijiWordDict = {
    'powered': [(27,526)],
    'unpowered': [(2,526)]
}
jijiWordDraw = drawInfo('JIJIWORD', 'spriteWord', 'saddleBrown', 'white', jijiWordDict)

meDict = {
    'right': [(52+25*i,751) for i in range(4)],
    'up': [(152+25*i,751) for i in range(4)],
    'left': [(252+25*i,751) for i in range(4)],
    'down': [(352+25*i,751) for i in range(4)]
}
meDraw = drawInfo('ME', 'sprite', 'saddleBrown', 'white', meDict)

meWordDict = {
    'powered': [(27,751)],
    'unpowered': [(2,751)]
}
meWordDraw = drawInfo('MEWORD', 'spriteWord', 'saddleBrown', 'white', meWordDict)

robotDict = {
    'right': [(52+25*i,901) for i in range(4)],
    'up': [(152+25*i,901) for i in range(4)],
    'left': [(252+25*i,901) for i in range(4)],
    'down': [(352+25*i,901) for i in range(4)]
}
robotDraw = drawInfo('ROBOT', 'sprite', 'saddleBrown', 'white', robotDict)

robotWordDict = {
    'powered': [(27,901)],
    'unpowered': [(2,901)]
}
robotWordDraw = drawInfo('ROBOTWORD', 'spriteWord', 'saddleBrown', 'white', robotWordDict)

itDict = {
    'right': [(52+25*i,451) for i in range(4)],
    'up': [(152+25*i,451) for i in range(4)],
    'left': [(252+25*i,451) for i in range(4)],
    'down': [(352+25*i,451) for i in range(4)]
}
itDraw = drawInfo('IT', 'sprite', 'saddleBrown', 'white', itDict)

itWordDict = {
    'powered': [(27,451)],
    'unpowered': [(2,451)]
}
itWordDraw = drawInfo('ITWORD', 'spriteWord', 'saddleBrown', 'white', itWordDict)

frogDict = {
    'right': [(52+25*i,376) for i in range(4)],
    'up': [(152+25*i,376) for i in range(4)],
    'left': [(252+25*i,376) for i in range(4)],
    'down': [(352+25*i,376) for i in range(4)]
}
frogDraw = drawInfo('FROG', 'sprite', 'saddleBrown', 'white', frogDict)

frogWordDict = {
    'powered': [(27,376)],
    'unpowered': [(2,376)]
}
frogWordDraw = drawInfo('FROGWORD', 'spriteWord', 'saddleBrown', 'white', frogWordDict)

eyeDict = {
    'right': [(52+25*i,226) for i in range(4)],
    'up': [(152+25*i,226) for i in range(4)],
    'left': [(252+25*i,226) for i in range(4)],
    'down': [(352+25*i,226) for i in range(4)]
}
eyeDraw = drawInfo('EYE', 'sprite', 'saddleBrown', 'white', eyeDict)

eyeWordDict = {
    'powered': [(27,226)],
    'unpowered': [(2,226)]
}
eyeWordDraw = drawInfo('EYEWORD', 'spriteWord', 'saddleBrown', 'white', eyeWordDict)



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

jellyDict = (851,301)
jellyDraw = drawInfo('JELLY', 'object', 'saddleBrown', 'white', jellyDict)

jellyWordDict = {
    'powered': [(826,301)],
    'unpowered': [(801,301)]
}
jellyWordDraw = drawInfo('JELLYWORD', 'objectWord', 'saddleBrown', 'white', jellyWordDict)

algaeDict = (101,1)
algaeDraw = drawInfo('ALGAE', 'object', 'saddleBrown', 'white', algaeDict)

algaeWordDict = {
    'powered': [(76,1)],
    'unpowered': [(51,1)]
}
algaeWordDraw = drawInfo('ALGAEWORD', 'objectWord', 'saddleBrown', 'white', algaeWordDict)

doorDict = (226,151)
doorDraw = drawInfo('DOOR', 'object', 'saddleBrown', 'white', doorDict)

doorWordDict = {
    'powered': [(201,151)],
    'unpowered': [(176,151)]
}
doorWordDraw = drawInfo('DOORWORD', 'objectWord', 'saddleBrown', 'white', doorWordDict)

keyDict = (101,376)
keyDraw = drawInfo('KEY', 'object', 'saddleBrown', 'white', keyDict)

keyWordDict = {
    'powered': [(76,376)],
    'unpowered': [(51,376)]
}
keyWordDraw = drawInfo('KEYWORD', 'objectWord', 'saddleBrown', 'white', keyWordDict)

treeDict = (476,751)
treeDraw = drawInfo('TREE', 'object', 'saddleBrown', 'white', treeDict)

treeWordDict = {
    'powered': [(451,751)],
    'unpowered': [(426,751)]
}
treeWordDraw = drawInfo('TREEWORD', 'objectWord', 'saddleBrown', 'white', treeWordDict)

leafDict = (601,376)
leafDraw = drawInfo('LEAF', 'object', 'saddleBrown', 'white', leafDict)

leafWordDict = {
    'powered': [(576,376)],
    'unpowered': [(551,376)]
}
leafWordDraw = drawInfo('LEAFWORD', 'objectWord', 'saddleBrown', 'white', leafWordDict)




#wall-related sprites--------------------------------
#yes, I could put this in a big dictionary with object:y-coordinate value pairs.
#But i'm too lazy and this thing is due in less than a week, so I'm leaving it as is. 
wallDict = {i:(73+25*i+1,1501) for i in range(16)}
wallDraw = drawInfo('WALL', 'wall', 'dimGrey', 'white', wallDict)

wallWordDict = {
    'powered': [(48,1501)],
    'unpowered': [(23,1501)]
}
wallWordDraw = drawInfo('WALLWORD', 'wallWord', 'dimGrey', 'white', wallWordDict)

waterDict = {i:(73+25*i+1,1576) for i in range(16)}
waterDraw = drawInfo('WATER', 'wall', 'blue', 'white', waterDict)

waterWordDict = {
    'powered': [(48,1576)],
    'unpowered': [(23,1576)]
}
waterWordDraw = drawInfo('WATERWORD', 'wallWord', 'blue', 'white', waterWordDict)

lavaDict = {i:(73+25*i+1,901) for i in range(16)}
lavaDraw = drawInfo('LAVA', 'wall', 'red', 'white', lavaDict)

lavaWordDict = {
    'powered': [(48,901)],
    'unpowered': [(23,901)]
}
lavaWordDraw = drawInfo('LAVAWORD', 'wallWord', 'red', 'white', lavaWordDict)

iceDict = {i:(73+25*i+1,826) for i in range(16)}
iceDraw = drawInfo('ICE', 'wall', 'white', 'white', iceDict)

iceWordDict = {
    'powered': [(48,826)],
    'unpowered': [(23,826)]
}
iceWordDraw = drawInfo('ICEWORD', 'wallWord', 'white', 'white', iceWordDict)

hedgeDict = {i:(73+25*i+1,751) for i in range(16)}
hedgeDraw = drawInfo('HEDGE', 'wall', 'saddleBrown', 'white', hedgeDict)

hedgeWordDict = {
    'powered': [(48,751)],
    'unpowered': [(23,751)]
}
hedgeWordDraw = drawInfo('HEDGEWORD', 'wallWord', 'saddleBrown', 'white', hedgeWordDict)

grassDict = {i:(73+25*i+1,676) for i in range(16)}
grassDraw = drawInfo('GRASS', 'wall', 'saddleBrown', 'white', grassDict)

grassWordDict = {
    'powered': [(48,676)],
    'unpowered': [(23,676)]
}
grassWordDraw = drawInfo('GRASSWORD', 'wallWord', 'saddleBrown', 'white', grassWordDict)

fenceDict = {i:(73+25*i+1,526) for i in range(16)}
fenceDraw = drawInfo('FENCE', 'wall', 'saddleBrown', 'white', fenceDict)

fenceWordDict = {
    'powered': [(48,526)],
    'unpowered': [(23,526)]
}
fenceWordDraw = drawInfo('FENCEWORD', 'wallWord', 'saddleBrown', 'white', fenceWordDict)   

brickDict = {i:(73+25*i+1,151) for i in range(16)}
brickDraw = drawInfo('BRICK', 'wall', 'saddleBrown', 'white', brickDict)

brickWordDict = {
    'powered': [(48,151)],
    'unpowered': [(23,151)]
}
brickWordDraw = drawInfo('BRICKWORD', 'wallWord', 'saddleBrown', 'white', brickWordDict)   

lineDict = {i:(73+25*i+1,976) for i in range(16)}
lineDraw = drawInfo('LINE', 'wall', 'saddleBrown', 'white', lineDict)

lineWordDict = {
    'powered': [(48,976)],
    'unpowered': [(23,976)]
} 
lineWordDraw = drawInfo('LINEWORD', 'wallWord', 'saddleBrown', 'white', lineWordDict)

pipeDict = {i:(73+25*i+1,1051) for i in range(16)}
pipeDraw = drawInfo('PIPE', 'wall', 'saddleBrown', 'white', pipeDict)

pipeWordDict = {
    'powered': [(48,1051)],
    'unpowered': [(23,1051)]
}
pipeWordDraw = drawInfo('PIPEWORD', 'wallWord', 'saddleBrown', 'white', pipeWordDict)


#object2(animated, *usually non player objects *)--------------------------------
beltDict = { #belt is the only 8-long player-esque object. 
    'right': [(476+25*i,85) for i in range(4)],
    'up': [(576+25*i,85) for i in range(4)],
    'left': [(676+25*i,85) for i in range(4)],
    'down': [(776+25*i,85) for i in range(4)]
}
beltDraw = drawInfo('BELT', 'object2', 'saddleBrown', 'white', beltDict)
beltWordDict = {
    'powered': [(451,85)],
    'unpowered': [(426,85)]
}
beltWordDraw = drawInfo('BELTWORD', 'object2Word', 'saddleBrown', 'white', beltWordDict)

skullDict = {
    'right': [(176,922)],
    'up': [(201,922)],
    'left': [(226,922)],
    'down': [(251,922)]
}
skullDraw = drawInfo('SKULL', 'object2', 'saddleBrown', 'white', skullDict)
skullWordDict = {
    'powered': [(151,922)],
    'unpowered': [(126,922)]
}
skullWordDraw = drawInfo('SKULLWORD', 'object2Word', 'saddleBrown', 'white', skullWordDict)

ghostDict = {
    'right': [(451,622)],
    'up': [(476,622)],
    'left': [(526,622)],
    'down': [(551,622)]
}
ghostDraw = drawInfo('GHOST', 'object2', 'saddleBrown', 'white', ghostDict)
ghostWordDict = {
    'powered': [(426,622)],
    'unpowered': [(401,622)]
}
ghostWordDraw = drawInfo('GHOSTWORD', 'object2Word', 'saddleBrown', 'white', ghostWordDict)

birdDict = {
    'right': [(176,322)],
    'up': [(201,322)],
    'left': [(226,322)],
    'down': [(251,322)]
}
birdDraw = drawInfo('BIRD', 'object2', 'saddleBrown', 'white', birdDict)
birdWordDict = {
    'powered': [(151,322)],
    'unpowered': [(126,322)]
}
birdWordDraw = drawInfo('BIRDWORD', 'object2Word', 'saddleBrown', 'white', birdWordDict)
boltDict = {
    'right': [(726,322)],
    'up': [(751,322)],
    'left': [(776,322)],
    'down': [(801,322)]
}
boltDraw = drawInfo('BOLT', 'object2', 'saddleBrown', 'white', boltDict)
boltWordDict = {
    'powered': [(701,322)],
    'unpowered': [(676,322)]
}
boltWordDraw = drawInfo('BOLTWORD', 'object2Word', 'saddleBrown', 'white', boltWordDict)
arrowDict = {
    'right': [(176,247)],
    'up': [(201,247)],
    'left': [(226,247)],
    'down': [(251,247)]
}
arrowDraw = drawInfo('ARROW', 'object2', 'saddleBrown', 'white', arrowDict)
arrowWordDict = {
    'powered': [(151,247)],
    'unpowered': [(126,247)]
}
arrowWordDraw = drawInfo('ARROWWORD', 'object2Word', 'saddleBrown', 'white', arrowWordDict)
rocketDict = {
    'right': [(176,847)],
    'up': [(201,847)],
    'left': [(226,847)],
    'down': [(251,847)]
}
rocketDraw = drawInfo('ROCKET', 'object2', 'saddleBrown', 'white', rocketDict)
rocketWordDict = {
    'powered': [(151,847)],
    'unpowered': [(126,847)]
}
rocketWordDraw = drawInfo('ROCKETWORD', 'object2Word', 'saddleBrown', 'white', rocketWordDict)


#words--------------------------------
equalsDict = {
    'powered': [(226.5,76)],
    'unpowered': [(251.5,76)]
}
equalsDraw = drawInfo('IS', 'word', 'black', 'white', equalsDict)

hasDict = {
    'powered': [(51.5,151)],
    'unpowered': [(26.5,151)]
}
hasDraw = drawInfo('HAS', 'word', 'black', 'white', hasDict)

notDict = {
    'powered': [(201.5,76)],
    'unpowered': [(176.5,76)]
}
notDraw = drawInfo('NOT', 'word', 'saddleBrown', 'white', notDict)

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

sinkDict = {
    'powered': [(51.5,805)],
    'unpowered': [(26.5,805)]
}
sinkDraw = drawInfo('SINK', 'word', 'saddleBrown', 'white', sinkDict)

defeatDict = {
    'powered': [(51.5,730)],
    'unpowered': [(26.5,730)]
}
defeatDraw = drawInfo('DEFEAT', 'word', 'saddleBrown', 'white', defeatDict)

hotDict = {
    'powered': [(126.5,730)],
    'unpowered': [(101.5,730)]
}
hotDraw = drawInfo('HOT', 'word', 'saddleBrown', 'white', hotDict)

meltDict = {
    'powered': [(201.5,730)],
    'unpowered': [(176.5,730)]
}
meltDraw = drawInfo('MELT', 'word', 'saddleBrown', 'white', meltDict)

openDict = {
    'powered': [(276.5,730)],
    'unpowered': [(251.5,730)]
}
openDraw = drawInfo('OPEN', 'word', 'saddleBrown', 'white', openDict)

shutDict = {
    'powered': [(351.5,730)],
    'unpowered': [(326.5,730)]
}
shutDraw = drawInfo('SHUT', 'word', 'saddleBrown', 'white', shutDict)

floatDict = {
    'powered': [(276.5,805)],
    'unpowered': [(251.5,805)]
}
floatDraw = drawInfo('FLOAT', 'word', 'saddleBrown', 'white', floatDict)

weakDict = {
    'powered': [(201.5,1123)],
    'unpowered': [(176.5,1123)]
}
weakDraw = drawInfo('WEAK', 'word', 'saddleBrown', 'white', weakDict)

eatDict = {
    'powered': [(126.5,151)],
    'unpowered': [(101.5,151)]
}
eatDraw = drawInfo('EAT', 'word', 'saddleBrown', 'white', eatDict)

hasDict = {
    'powered': [(176.5,76)],
    'unpowered': [(201.5,76)]
}
hasDraw = drawInfo('HAS', 'word', 'saddleBrown', 'white', hasDict)

andDict = {
    'powered': [(351.5,76)],
    'unpowered': [(326.5,76)]
}
andDraw = drawInfo('AND', 'word', 'saddleBrown', 'white', andDict)

emptyDict = {
    'powered': [(126.5,76)],
    'unpowered': [(101.5,76)]
}
emptyDraw = drawInfo('EMPTY', 'word', 'saddleBrown', 'white', emptyDict)

onDict = {
    'powered': [(51.5,151)],
    'unpowered': [(26.5,1273)]
}
onDraw = drawInfo('ON', 'word', 'saddleBrown', 'white', onDict)

lonelyDict = {
    'powered': [(201.5,1198)],
    'unpowered': [(176.5,1198)]
}
lonelyDraw = drawInfo('LONELY', 'word', 'saddleBrown', 'white', lonelyDict)

doneDict = {
    'powered': [(51.5,1873)],
    'unpowered': [(26.5,1873)]
}
doneDraw = drawInfo('DONE', 'word', 'saddleBrown', 'white', doneDict)

allDict = {
    'powered': [(51.5,1)],
    'unpowered': [(26.5,1)]
}
allDraw = drawInfo('ALL', 'word', 'saddleBrown', 'white', allDict)

textWordDraw = {
    'powered': [(126.5,1)],
    'unpowered': [(101.5,1)]
}
textWordDraw = drawInfo('TEXTWORD', 'word', 'saddleBrown', 'white', textWordDraw)

levelWordDraw = {
    'powered': [(201.5,1)],
    'unpowered': [(176.5,1)]
}
levelWordDraw = drawInfo('LEVELWORD', 'word', 'saddleBrown', 'white', levelWordDraw)

moveWordDraw = {
    'powered': [(276.5,301)],
    'unpowered': [(251.5,301)]
}
moveWordDraw = drawInfo('MOVEWORD', 'word', 'saddleBrown', 'white', moveWordDraw)

moreWordDraw = {
    'powered': [(351.5,1123)],
    'unpowered': [(326.5,1123)]
}
moreWordDraw = drawInfo('MOREWORD', 'word', 'saddleBrown', 'white', moreWordDraw)

shiftWordDraw = {
    'powered': [(351.5,301)],
    'unpowered': [(326.5,301)]
}
shiftWordDraw = drawInfo('SHIFTWORD', 'word', 'saddleBrown', 'white', shiftWordDraw)

openWordDraw = {
    'powered': [(276.5,730)],
    'unpowered': [(251.5,730)]
}
openWordDraw = drawInfo('OPENWORD', 'word', 'saddleBrown', 'white', openWordDraw)

shutWordDraw = {
    'powered': [(351.5,730)],
    'unpowered': [(326.5,730)]
}
shutWordDraw = drawInfo('SHUTWORD', 'word', 'saddleBrown', 'white', shutWordDraw)



