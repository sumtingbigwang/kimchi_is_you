from random import randint
from cmu_graphics import *
from model.objects import *
from model.lookup import *

def playRandomMoveSound():
    randIdx = randint(47,58)
    Sound(f'sounds/move/0{randIdx}.ogg').play()
    
def playRandomUndoSound():
    randIdx = randint(43,46)
    Sound(f'sounds/undo/0{randIdx}.ogg').play()
    
def playRandomRuleSound():
    randIdx = randint(35,39)
    Sound(f'sounds/maderule/{randIdx}.mp3').play()
    
def playRandomSinkSound():
    randIdx = randint(23,29)
    Sound(f'sounds/sink/{randIdx}.ogg').play()

def playRandomDefeatSound():
    randIdx = randint(6,11)
    Sound(f'sounds/defeat/{randIdx}.mp3').play()

def playRandomMeltSound():
    randIdx = randint(117,119)
    Sound(f'sounds/melt/{randIdx}.mp3').play()
    
def checkRuleSound(wordObject):
    if wordObject.powered:
        print('rule sound')
        playRandomRuleSound()