from cmu_graphics import * 
from PIL import Image
#We want ALL OF THE SPRITE DRAW DATA HERE. E.G.
class drawInfo:
    #replace the following with sprite image links. should be (self, position1, position2, position3)
    def __init__(self, name, color, labelcolor):
        self.name = name
        self.color = color
        self.labelcolor = labelcolor

#crop radius: 24x24
#barrier: 1 pixel 
#starts at (1,1)
#crop: corners, top left and bottom right
#have a 2D list of images, each row is up/right/left/right animation
#down
babaDraw = drawInfo('BABA', 'grey', 'white')
rockDraw = drawInfo('ROCK', 'saddleBrown', 'white')
wallDraw = drawInfo('WALL', 'dimGrey', 'white')
flagDraw = drawInfo('FLAG', 'gold', 'white')

babaWordDraw = drawInfo('BABA', 'grey', 'white')
rockWordDraw = drawInfo('ROCK', 'saddleBrown', 'white')
wallWordDraw = drawInfo('WALL', 'dimGrey', 'white')
flagWordDraw = drawInfo('FLAG', 'gold', 'white')

equalsDraw = drawInfo('IS', 'black', 'white')
hasDraw = drawInfo('HAS', 'black', 'white')

youDraw = drawInfo('YOU', 'grey', 'white')
pushDraw = drawInfo('PUSH', 'saddleBrown', 'white')
stopDraw = drawInfo('STOP', 'dimGrey', 'white')
winDraw = drawInfo('WIN', 'gold', 'white')



