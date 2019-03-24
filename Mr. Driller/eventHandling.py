from level import *
from pygame.locals import *


def keydownHandle(event, surface):

    if event.key == K_g:
        newLvl = generateLvl(4, 2, 4)
        pygameRender(surface, newLvl)