from random import randint
from cmu_graphics import *

def playRandomMoveSound():
    randIdx = randint(47,58)
    Sound(f'sounds/move/0{randIdx}.ogg').play()
    
def playRandomUndoSound():
    randIdx = randint(43,46)
    Sound(f'sounds/undo/0{randIdx}.ogg').play()