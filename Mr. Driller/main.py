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
    player = Character(6, 8)
    currentLine = 0
    level = generateLvl(4, 9, 7)
    print(len(level))

    # Initializing controls
    if 'nt' in os.name:
        movKeys = [K_w, K_d, K_a]
    elif 'ix' in os.name:
        movKeys = [K_z, K_d, K_q]

    arrowKeys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

    # Main loop
    inProgress = True
    while inProgress:
        for event in pygame.event.get():

            if event.type == QUIT:
                inProgress = False

            if event.type == KEYDOWN:
                if event.key in movKeys:    # Movement
                    movementHandle(event, surface, player, level, movKeys)
                elif event.key in arrowKeys:    # Block breaking
                    breaking(event, surface, player, level)
                elif event.key == K_r:
                    player.display(surface)
                else:
                    currentLine = keydownHandle(event, currentLine, surface, level)

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)


