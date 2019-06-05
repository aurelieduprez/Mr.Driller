import pygame
from character import *
from level import *
from os import name, path
from eventHandling import *
from menu import *
from block import *

# Font and Sound verification

if not pygame.font:
    print('Warning : font off')
if not pygame.mixer:
    print('Warning : sound off')
pygame.mixer.init(44100, 16, 2, 1024)


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

    nbFrame = 1

    blocksDisap = []
    levelID = 1
    levelDepth = 25

    player = Character(3, 4, levelID, 0)    # Creates the player instance(posX, posY, bckgrnd, lives)
    level = generateLvl(4, levelDepth, 7, levelID)   # Generates Lvl (nmb colors, depth, width, bckgrns)

    evChgLvl = pygame.event.Event(pygame.USEREVENT, attr1="evChgLvl")

    # State of the Game
    inPause = False
    inMenu = True
    optionIM = 1
    inProgress = True
    isDead = False
    optionID = 0
    hasToInit = True

    # Initializing Ui
    FontUi = pygame.font.Font("Assets\Misc\police\Act_Of_Rejection.ttf", 36)
    Ui_bg = pygame.image.load(path.join("Assets", "Misc", "userinterface.png"))
    fileName = str(player.oxyAcc())
    fileName += ".png"
    oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))
    Oxygen_display = FontUi.render(str(player.oxyAcc()), 1, (220, 0, 255))
    music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
    pygame.mixer.music.play(-1, 0)

    # Initializing controls
    if 'nt' in name:
        movKeys = [K_w, K_d, K_a, K_s]
    elif 'ix' in name:
        movKeys = [K_z, K_d, K_q, K_s]

    arrowKeys = [K_UP, K_DOWN, K_LEFT, K_RIGHT]

    # Updating Connected textures
    for line in level:
        for element in line:
            element.updCoText(level)

    # Main loop
    while inProgress:
        if player.livesAcc() < 0 and not isDead and not inMenu and not inPause and not hasToInit and optionID == 0:
            isDead = True
            deathScreen = pygame.image.load(path.join("Assets", "Splash", "death1.png"))
            surface.blit(deathScreen, (0, 0))
            optionID = 1

        if not inPause and not inMenu and not isDead:

            # Rendering level and displaying player
            render(surface, level, currentOffset)
            player.Anim(surface)
            player.display(surface)

        if inMenu:
            mainMenu(surface, optionIM)

        for event in pygame.event.get():
            nbFrameAnim = 1     # reset FrameCount for anim

            if event.type == QUIT:  # Quitting the game
                inPause = False
                inProgress = False

            if event == evChgLvl:
                # Displays splash for 3 secs
                splashName = "level"
                splashName += str(levelID+1)
                splashName += ".png"
                splashImg = pygame.image.load(path.join("Assets", "Splash", splashName))
                surface.blit(splashImg, (0, 0))
                pygame.display.update()
                pygame.time.wait(3000)

                # Actually changes Lvl
                level, levelID = changeLvl(levelID, player)
                currentBotLine = 8
                currentOffset = 0
                currentClimb = 0
                blocksDisap = []
                backDown = False

            if event.type == KEYDOWN:       # Event handling
                # Test key for revive :P
                if event.key == K_UP and not inPause and not inMenu and not isDead:
                    player.AddScore(1000)

                if event.key == K_ESCAPE:
                    if not inPause and not inMenu and not isDead:
                        inPause = True
                        option = 1
                        optionFile = str(option)
                        optionFile += ".png"
                        pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                        surface.blit(pauseImage, (0, 0))

                    elif inPause:
                        inPause = False
                        render(surface, level, currentOffset)
                        player.display(surface)

                    elif isDead:
                        inMenu = True

                if event.key in movKeys:    # Movement
                    if not inPause and not inMenu and not isDead:
                        movementHandle(event, surface, player, level, movKeys)

                    elif inPause:
                        if event.key == movKeys[3] and option < 3:
                            render(surface, level, currentOffset)
                            player.Anim(surface)
                            player.display(surface)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            surface.blit(Oxygen_display, (640, 200))
                            surface.blit(oxyImage, (537, 252))
                            surface.blit(Depth_display, (640, 377))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            option += 1
                            optionFile = str(option)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                        if event.key == movKeys[0] and option > 1:
                            render(surface, level, currentOffset)
                            player.Anim(surface)
                            player.display(surface)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            surface.blit(Oxygen_display, (640, 200))
                            surface.blit(oxyImage, (537, 252))
                            surface.blit(Depth_display, (640, 377))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            option -= 1
                            optionFile = str(option)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                    elif isDead:
                        if event.key == movKeys[3] and optionID == 1:
                            render(surface, level, currentOffset)
                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            optionID += 1
                            optionFile = "death"
                            optionFile += str(optionID)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Splash", optionFile))
                            surface.blit(pauseImage, (0, 0))

                        elif event.key == movKeys[0] and optionID == 2:
                            render(surface, level, currentOffset)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            optionID -= 1
                            optionFile = "death"
                            optionFile += str(optionID)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Splash", optionFile))
                            surface.blit(pauseImage, (0, 0))

                elif event.key in arrowKeys:    # Block breaking
                    if not inPause and not inMenu and not isDead:
                        breaking(event, surface, player, level, currentBotLine)

                    elif inPause:
                        if event.key in [K_DOWN, movKeys[3]] and option < 3:
                            render(surface, level, currentOffset)
                            player.Anim(surface)
                            player.display(surface)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            surface.blit(Oxygen_display, (640, 200))
                            surface.blit(oxyImage, (537, 252))
                            surface.blit(Depth_display, (640, 377))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            option += 1
                            optionFile = str(option)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                        if event.key in [K_UP, movKeys[0]] and option > 1:
                            render(surface, level, currentOffset)
                            player.Anim(surface)
                            player.display(surface)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            surface.blit(Oxygen_display, (640, 200))
                            surface.blit(oxyImage, (537, 252))
                            surface.blit(Depth_display, (640, 377))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            option -= 1
                            optionFile = str(option)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                    elif inMenu:
                        if event.key == K_UP and optionIM == 2:
                            optionIM = 1
                            mainMenu(surface, optionIM)
                        elif event.key == K_DOWN and optionIM == 1:
                            optionIM = 2
                            mainMenu(surface, optionIM)

                    elif isDead:
                        if event.key == K_DOWN and optionID == 1:
                            render(surface, level, currentOffset)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            optionID += 1
                            optionFile = "death"
                            optionFile += str(optionID)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Splash", optionFile))
                            surface.blit(pauseImage, (0, 0))

                        elif event.key == K_UP and optionID == 2:
                            render(surface, level, currentOffset)

                            surface.blit(Ui_bg, (0, 0))
                            surface.blit(score_display, (640, 107))
                            for i in range(0, player.livesAcc()):
                                surface.blit(icon, (700 - i * 70, 500))

                            optionID -= 1
                            optionFile = "death"
                            optionFile += str(optionID)
                            optionFile += ".png"
                            pauseImage = pygame.image.load(path.join("Assets", "Splash", optionFile))
                            surface.blit(pauseImage, (0, 0))

                elif event.key == K_RETURN:
                    if inPause:
                        if option == 1:
                            inPause = False
                            render(surface, level, currentOffset)
                            player.display(surface)

                        elif option == 2:
                            inPause = False
                            level, levelID = restart(player)
                            currentBotLine = 8
                            currentOffset = 0
                            currentClimb = 0
                            blocksDisap = []
                            backDown = False
                            splashLvl1 = pygame.image.load(path.join("Assets", "Splash", "level1.png"))
                            surface.blit(splashLvl1, (0, 0))
                            pygame.display.update()
                            pygame.time.wait(3000)

                        elif option == 3:
                            inPause = False
                            inMenu = True

                    elif inMenu:
                        if optionIM == 1:
                            splashLvl1 = pygame.image.load(path.join("Assets", "Splash", "level1.png"))
                            surface.blit(splashLvl1, (0, 0))
                            pygame.display.update()
                            pygame.time.wait(3000)
                            inMenu = False
                            hasToInit = False

                        elif optionIM == 2:
                            inProgress = False

                    elif isDead:
                        if optionID == 1:
                            print("restart")

                        elif optionID == 2:
                            inMenu = True
                            isDead = False

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
        if not isDead and not inPause and not inMenu:
            player.fall(surface, level)

        if player.blocksFallenAcc() != currentOffset and not inMenu and not inPause and not isDead:
            currentOffset += 1
            currentBotLine += 1

            for i in range(0, len(level), 1):
                for element in level[i]:
                    element.updOffset(currentOffset)

        # Timed actions

        if nbFrame % 30 == 1 and not inPause and not inMenu and not isDead:   # Once per second
            player.updateOxygen(1, surface, level)
            for item in blocksDisap:
                if level[item[0]][item[1]].hpAccess() > 0:
                    level[item[0]][item[1]].timeout(surface, currentOffset)
                elif level[item[0]][item[1]].hpAccess() == 0:
                    del(blocksDisap[blocksDisap.index(item)])

        fileName = str(player.oxyAcc())
        fileName += ".png"
        oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))
        Oxygen_display = FontUi.render(str(player.oxyAcc()), 1, (220, 0, 255))

        if nbFrame % 5 == 1 and not inPause and not inMenu and not isDead:    # 6 times per second
            player.Anim(surface)
            render(surface, level, currentOffset)
            player.display(surface)
            for i in range(0, len(level), 1):
                for element in level[i]:
                    if element.typeAccess() == "delayed":
                        if element.idAcc() and element.hpAccess() > 0:
                            if player.blocksFallenAcc() != currentOffset:
                                currentOffset += 1
                                currentBotLine += 1
                            element.updOffset(currentOffset)
                            posY, posX = element.posAcc()
                            bDis = [posY, posX]
                            if bDis not in blocksDisap:
                                blocksDisap.append(bDis)

        if not player.IdlingAcc() and not inPause and not inMenu and not isDead:   # check if player is already idling
            nbFrameAnim += 1

        if nbFrameAnim % 10 == 1 and not inPause and not inMenu and not isDead:
            player.NeedToIdle(surface)

        if player.scoreAcc() < 1000:
            score_display = FontUi.render(str(player.scoreAcc()), 1, (220, 0, 255))
        elif player.scoreAcc() < 100000:
            score_display = FontUi.render(str((player.scoreAcc())/1000)+" k", 1, (220, 0, 255))
        else:
            score_display = FontUi.render(str(int((player.scoreAcc())/1000)) + " k", 1, (220, 0, 255))

        Depth_display = FontUi.render(str(currentOffset-player.climbAcc()), 1, (220, 0, 255))

        if not inPause and not inMenu and not isDead:
            surface.blit(Ui_bg, (0, 0))
            surface.blit(score_display, (640, 107))
            surface.blit(Oxygen_display, (640, 200))
            surface.blit(oxyImage, (537, 252))
            surface.blit(Depth_display, (640, 377))

            # Lives display
            for i in range(0, player.livesAcc()):
                surface.blit(icon, (700-i*70, 500))

        currentDepth = currentOffset - player.climbAcc()
        nbFrame += 1
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)


