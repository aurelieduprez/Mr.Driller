from level import *
from pygame.locals import *


def keydownHandle(event):
    
    if event.key == K_g:
        newLvl = generateLvl(4, 2, 4)
        displayLvLTxt(newLvl)