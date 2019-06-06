from pygame.locals import *


def movementHandle(event, surface, player, level, movKeys):

    if event.key == movKeys[2]:
        player.move(surface, 4, level)
    elif event.key == movKeys[1]:
        player.move(surface, 2, level)
    elif event.key == movKeys[0]:
        player.move(surface, 1, level)


def breaking(event, surface, player, level, currentBotLine):

    if event.key == K_RIGHT:
        player.breakBlock(surface, 2, level, currentBotLine)
    elif event.key == K_DOWN:
        player.breakBlock(surface, 3, level, currentBotLine)
    elif event.key == K_LEFT:
        player.breakBlock(surface, 4, level, currentBotLine)

