import pygame
from character import *
from level import *
from os import name
from eventHandling import *
from menu import *

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
    icon = pygame.image.load("Assets\Misc\icon.png")
    pygame.display.set_icon(icon)

    # Initializing useful variables
    currentBotLine = 8
    currentOffset = 0
    currentClimb = 0
    backDown = False
    player = Character(4, 4, currentBotLine, surface, lives=2)    # Creates the player instance
    level = generateLvl(4, 100, 7)
    PauseMenu = pygame.image.load("Assets\Menu\menupause.png")
    isPaused = False
    print(len(level))
    nbFrame = 1

    # Initializing controls
    if 'nt' in name:
        movKeys = [K_w, K_d, K_a]
    elif 'ix' in name:
        movKeys = [K_z, K_d, K_q]

    arrowKeys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

    # Update Connected textures

    for line in level:
        for element in line:
            element.updCoText(level)
    # Main loop
    inProgress = True
    while inProgress:
        # Rendering level and displaying player
        render(surface, level, currentOffset)
        player.Anim(surface)
        player.display(surface)
        for event in pygame.event.get():
            nbFrameAnim = 1 #reset FrameCount for anim


            if event.type == QUIT:      # Quitting the game
                inProgress = False

            if event.type == KEYDOWN:       # Event handling

                if event.key == K_ESCAPE:
                    if not isPaused:
                        isPaused = True
                        surface.blit(PauseMenu,(0,0))


                if event.key in movKeys:    # Movement
                    movementHandle(event, surface, player, level, movKeys)
                elif event.key in arrowKeys:    # Block breaking
                    breaking(event, surface, player, level, currentBotLine)
                else:
                    keydownHandle(event)

        # Cleanup after a climb

        if backDown and player.climbAcc() < currentClimb:
            if currentClimb == 0:
                backDown = False
            player.backDownCleanup(surface)

        currentClimb = player.climbAcc()

        if player.climbAcc() > 0:
            backDown = True

        # Updating blocks when falling

        player.fall(surface, level)

        if player.blocksFallenAcc() != currentOffset:
            currentOffset += 1
            currentBotLine += 1

            for i in range(0, len(level), 1):
                for element in level[i]:
                    element.updOffset(currentOffset)


        if nbFrame % 30== 1:
            player.updateOxygen(1, surface)
            print("oxygen =", player.oxyAcc())

        if player.IdlingAcc() == False: #check if player is already idling
            nbFrameAnim = nbFrameAnim + 1

            #if not x frame later it will play the "idle" animation
            if nbFrameAnim % 15 == 1:
                player.NeedToIdle(surface)

        nbFrame=nbFrame+1

        pygame.display.update()
        fpsClock.tick(FPS)

        while isPaused == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    isPaused = False
                    inProgress = False

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        isPaused = False
                        render(surface, level, currentOffset)
                        player.display(surface)
                    else:
                        keydownHandle(event)

                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()

                    if 287 < x < 530 and 218 < y < 279: #coordonées Resume
                        isPaused = False
                        render(surface, level, currentOffset)
                        player.display(surface)

                    elif 306 < x < 516 and 306 < y < 360: #coordonnées Restart
                        print("Restart")

                    elif 341 < x < 475 and 395 < y < 450: #coordonnées Quit
                        isPaused = False
                        inProgress = False


    pygame.quit()


game(800, 600)


