import pygame
from character import *
from level import *
from os import name, path
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
    player = Character(3, 4, currentBotLine, surface, lives=2)    # Creates the player instance
    level = generateLvl(4, 100, 7)
    print(len(level))
    nbFrame = 1

    #initialising Ui
    FontUi1 = pygame.font.Font("Assets\Misc\police\Act_Of_Rejection.ttf", 36)
    FontUi2 = pygame.font.Font("Assets\Misc\police\Act_Of_Rejection.ttf", 36)

    Ui_bg = pygame.image.load(path.join("Assets", "Misc", "userinterface.png"))


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

            if event.type == QUIT:  # Quitting the game
                inProgress = False

            if event.type == KEYDOWN:
                # Event handling
                # Test key for revive :P
                if event.key == K_UP:
                    player.AddScore(1000)
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

        if nbFrame % 30 == 1:
            player.updateOxygen(1, surface)

            fileName = str(player.oxyAcc())
            fileName += ".png"

            oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))

            Oxygen_display = FontUi2.render(str(player.oxyAcc()), 1, (220, 0, 255))

        if nbFrame % 5 == 1:
            player.Anim(surface)
            render(surface, level, currentOffset)
            player.display(surface)

        if not player.IdlingAcc(): #check if player is already idling
            nbFrameAnim += 1

        if nbFrameAnim % 10 == 1:
            player.NeedToIdle(surface)

        if player.scoreAcc() < 1000:
            score_display = FontUi2.render(str(player.scoreAcc()), 1, (220, 0, 255))
        elif player.scoreAcc() < 100000:
            score_display = FontUi2.render(str((player.scoreAcc())/1000)+" k", 1, (220, 0, 255))
        else:
            score_display = FontUi2.render(str(int((player.scoreAcc())/1000)) + " k", 1, (220, 0, 255))

        surface.blit(Ui_bg, (0, 0))
        surface.blit(score_display, (640, 107))
        surface.blit(Oxygen_display, (640, 200))
        surface.blit(oxyImage, (537, 252))

        nbFrame += 1

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)


