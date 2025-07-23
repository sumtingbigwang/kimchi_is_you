from numpy import * 
from model.objects import * 

    
#COORDINATES MUST BE OFFSET BY 1! THE LEVEL STARTS AT (0,0)!
#levels----------------------
equalsDict0 = {eq(None, None, False, 'black'):{(0,i)} for i in range(3)}
l0Dict = {'size':(10,5)} 
l0Dict.update(equalsDict0)
level0 = level(0, l0Dict,equalsDict0)
# flag.addEffect('PUSH')
# baba.addEffect('YOU')

equalsPos1 = {(4,1), (4,10),(12,1),(12,10)}
equalsDict1 = {eq(None, None, False, 'black'):{pos} for pos in equalsPos1}

youPos1 = {(5,1)}
youDict1 = {effect('YOU', False,'black'):{pos} for pos in youPos1}

l1Dict = {'size':(17,13),
        flag:{(12,6)},
        wall:({(i,4) for i in range(3,14)} | {(i,8) for i in range(3,14)}),
        baba:{(4,6)},
        rock:{(8,5),(8,6),(8,7)},
        babaw:{(3,1)},
        flagw:{(3,10)},
        rockw:{(11,1)},
        wallw:{(11,10)},
        push:{(13,1)},
        stop:{(13,10)},
        win:{(5,10)}
        }

l1Dict.update(equalsDict1)
l1Dict.update(youDict1)

level1 = level(1,l1Dict,equalsDict1)