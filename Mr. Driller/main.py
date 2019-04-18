import pygame, sys
from eventHandling import *

# Font and Sound verification

if not pygame.font:
    print('Warning : font off')
if not pygame.mixer:
    print('Warning : sound off')


def game(x, y):

    # Initializing pyGame & FPS
    pygame.init()
    FPS = 30
    fpsClock = pygame.time.Clock()
    surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption('Mr. Driller')

    # Initializing useful variables
    player = Character(2, 2)
    currentLine = 0
    level = generateLvl(4, 9, 7)
    print(len(level))
    if 'nt' in os.name:
        movKeys = [K_w, K_d, K_a]
    elif 'ix' in os.name:
        movKeys = [K_z, K_d, K_q]

    # Main loop
    inProgress = True
    while inProgress:
        for event in pygame.event.get():

            if event.type == QUIT:
                inProgress = False

            if event.type == KEYDOWN:
                if event.key in movKeys:
                    movementHandle(event, surface, player, level, movKeys)
                elif event.key == K_r:
                    player.display(surface)
                else:
                    currentLine = keydownHandle(event, currentLine, surface, level)

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)


