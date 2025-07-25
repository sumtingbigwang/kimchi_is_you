#We want ALL OF THE SPRITE DRAW DATA HERE. E.G.
class drawInfo:
    #replace the following with sprite image links. should be (self, position1, position2, position3)
    def __init__(self, name, color, labelcolor):
        self.name = name
        self.color = color
        self.labelcolor = labelcolor


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



