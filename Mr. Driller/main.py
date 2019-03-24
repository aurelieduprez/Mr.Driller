import pygame, sys
from eventHandling import *


def game(x, y):

    # Initializing pyGame
    pygame.init()
    surface = pygame.display.set_mode((x, y))
    pygame.display.set_caption('Mr. Driller')

    # Main loop
    inProgress = True
    while inProgress:
        for event in pygame.event.get():
            if event.type == QUIT:
                inProgress = False

            if event.type == KEYDOWN:
                keydownHandle(event, surface)

        pygame.display.update()
    pygame.quit()


game(800, 600)


