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
    blocksFall = []
    levelID = 1

    player = Character(3, 4, levelID, 0)    # Creates the player instance(posX, posY, bckgrnd, lives)
    level = []

    # Custom Events
    EVCHGLVL = USEREVENT
    EVSECOND = USEREVENT+1

    evChgLvl = pygame.event.Event(EVCHGLVL)
    evSecond = pygame.event.Event(EVSECOND)

    # Timers
    pygame.time.set_timer(USEREVENT+1, 1100)

    # State of the Game
    inPause = False
    inMenu = True
    inGame = False
    optionIM = 1
    inProgress = True
    isDead = False
    optionID = 0
    hasToInit = True
    won = False
    ws = 0

    # Initializing Ui
    FontUi = pygame.font.Font("Assets\Misc\police\Act_Of_Rejection.ttf", 36)
    Ui_bg = pygame.image.load(path.join("Assets", "Misc", "userinterface.png"))
    fileName = str(player.oxyAcc())
    fileName += ".png"
    oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))
    Oxygen_display = FontUi.render(str(player.oxyAcc()), 1, (220, 0, 255))
    music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
    pygame.mixer.music.set_volume(0.50)
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
            deathScreen = pygame.image.load(path.join("Assets", "Menu", "death1.png"))
            surface.blit(deathScreen, (0, 0))
            optionID = 1

        if won:
            if ws == 0:
                ws = 1
                surface.fill((0, 0, 0))
                music = pygame.mixer.music.load(path.join("Assets", "Music", "win.wav"))
                pygame.mixer.music.play(-1, 0)
                winScreen1 = pygame.image.load(path.join("Assets", "Splash", "win1.png"))
                surface.blit(winScreen1, (0, 0))
                pygame.display.update()

            elif ws == 2:
                ws = 3
                surface.fill((0, 0, 0))
                winScreen1 = pygame.image.load(path.join("Assets", "Splash", "win2.png"))
                surface.blit(winScreen1, (0, 0))
                pygame.display.update()

        if not inPause and not inMenu and not isDead and not won:

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

            if event.type == USEREVENT:
                if levelID < 10:
                    # Displays splash for 3 secs
                    splashName = "level"
                    splashName += str(levelID+1)
                    splashName += ".png"
                    musicName = "Level"
                    musicName += str(levelID + 1)
                    musicName += ".wav"
                    splashImg = pygame.image.load(path.join("Assets", "Splash", splashName))
                    music = pygame.mixer.music.load(path.join("Assets", "Music", musicName))
                    pygame.mixer.music.play(-1, 0)
                    surface.blit(splashImg, (0, 0))
                    pygame.display.update()
                    pygame.time.wait(3000)

                    # Actually changes Lvl
                    level, levelID, won = changeLvl(levelID, player)
                    currentBotLine = 8
                    currentOffset = 0
                    currentClimb = 0
                    blocksDisap = []
                    backDown = False

                else:
                    won = True
                    storeScore(player.scoreAcc())

            if event.type == EVSECOND and inGame:  # Once per second
                if levelID <= 4:  # Updates oxygen
                    player.updateOxygen(1, surface, level)
                for item in blocksDisap:  # Updates block that are be disappearing
                    if level[item[0]][item[1]].hpAccess() > 0:
                        level[item[0]][item[1]].timeout(surface)
                    elif level[item[0]][item[1]].hpAccess() == 0:
                        del (blocksDisap[blocksDisap.index(item)])
                for item in blocksFall:
                    if level[item[0]][item[1]].holdAccess() > 0:
                        level[item[0]][item[1]].fallTick()
                    elif level[item[0]][item[1]].holdAccess() == 0:
                        level[item[0]+1][item[1]] = level[item[0]][item[1]]
                        level[item[0]][item[1]].fall(surface, level)
                        level[item[0]][item[1]] = block.Classic(item[0], item[1], 1, 0)
                        level[item[0]][item[1]].changeBG(levelID)
                        level[item[0]][item[1]].display(surface)
                        #del (blocksDisap[blocksFall.index(item)])

                print(blocksFall)

            if event.type == KEYDOWN:       # Event handling

                if event.key == K_ESCAPE:
                    if not inPause and not inMenu and not isDead and not won:
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

                    elif won:
                        inMenu = True
                        won = False
                        music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                        pygame.mixer.music.play(-1, 0)

                if event.key in movKeys:    # Movement

                    if not inPause and not inMenu and not isDead and not won:
                        inGame = True
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
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
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
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                elif event.key in arrowKeys:    # Block breaking
                    if not inPause and not inMenu and not isDead and not won:
                        inGame = True
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
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
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
                            pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                            surface.blit(pauseImage, (0, 0))

                elif event.key == K_RETURN:
                    if inPause:
                        if option == 1:
                            inPause = False
                            render(surface, level, currentOffset)
                            player.display(surface)

                        elif option == 2:
                            inPause = False
                            level, levelID, won = restart(player)
                            currentBotLine = 8
                            currentOffset = 0
                            currentClimb = 0
                            blocksDisap = []
                            backDown = False
                            splashLvl1 = pygame.image.load(path.join("Assets", "Splash", "level1.png"))
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "Level1.wav"))
                            pygame.mixer.music.play(-1, 0)
                            surface.blit(splashLvl1, (0, 0))
                            pygame.display.update()
                            pygame.time.wait(3000)

                        elif option == 3:
                            mainMenu(surface, optionIM)
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                            pygame.mixer.music.play(-1, 0)
                            inPause = False
                            inMenu = True

                    elif inMenu:
                        if optionIM == 1:
                            level, levelID, won = restart(player)
                            currentBotLine = 8
                            currentOffset = 0
                            currentClimb = 0
                            blocksDisap = []
                            backDown = False
                            splashLvl1 = pygame.image.load(path.join("Assets", "Splash", "level1.png"))
                            surface.blit(splashLvl1, (0, 0))
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "Level1.wav"))
                            pygame.mixer.music.play(-1, 0)
                            pygame.display.update()
                            pygame.time.wait(3000)
                            inMenu = False
                            hasToInit = False

                        elif optionIM == 2:
                            inProgress = False

                    elif isDead:
                        if optionID == 1:
                            isDead = False
                            level, levelID, won = restart(player)
                            currentBotLine = 8
                            currentOffset = 0
                            currentClimb = 0
                            blocksDisap = []
                            backDown = False
                            splashLvl1 = pygame.image.load(path.join("Assets", "Splash", "level1.png"))
                            surface.blit(splashLvl1, (0, 0))
                            pygame.display.update()
                            pygame.time.wait(3000)

                        elif optionID == 2:
                            inMenu = True
                            isDead = False

                    elif won:
                        if ws == 1:
                            ws = 2
                        elif ws == 3:
                            inMenu = True
                            won = False
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                            pygame.mixer.music.play(-1, 0)

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
        if not isDead and not inPause and not inMenu and not isDead and not won:
            player.fall(surface, level)

        if player.blocksFallenAcc() != currentOffset and not inMenu and not inPause and not isDead and not won:
            currentOffset += 1
            currentBotLine += 1

            for i in range(0, len(level), 1):
                for element in level[i]:
                    element.updOffset(currentOffset)

        # Timed actions

        if nbFrame % 25 == 1 and not inPause and not inMenu and not isDead and not won:   # Once per second
            if levelID > 4:
                player.updateOxygen(1, surface, level)
                
        fileName = str(player.oxyAcc())
        fileName += ".png"
        oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))
        Oxygen_display = FontUi.render(str(player.oxyAcc()), 1, (220, 0, 255))

        if nbFrame % 5 == 1 and not inPause and not inMenu and not isDead and not won:    # 6 times per second
            # Player Animations
            player.Anim(surface)
            render(surface, level, currentOffset)
            player.display(surface)

            # Checking Level
            for i in range(0, len(level), 1):
                for element in level[i]:
                    # Making delayed blocks disappear
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
                    if 4 < i < len(level)-5:
                        element.checkFall(level)
                        if element.fallAccess():
                            posY, posX = element.posAcc()
                            bFa = [posY, posX]
                            if bFa not in blocksFall:
                                blocksFall.append(bFa)

        if not player.IdlingAcc() and not inPause and not inMenu and not isDead and not won:   # check if player is already idling
            nbFrameAnim += 1

        if nbFrameAnim % 10 == 1 and not inPause and not inMenu and not isDead and not won:
            player.NeedToIdle(surface)

        if player.scoreAcc() < 1000:
            score_display = FontUi.render(str(player.scoreAcc()), 1, (220, 0, 255))
        elif player.scoreAcc() < 100000:
            score_display = FontUi.render(str((player.scoreAcc())/1000)+" k", 1, (220, 0, 255))
        else:
            score_display = FontUi.render(str(int((player.scoreAcc())/1000)) + " k", 1, (220, 0, 255))

        Depth_display = FontUi.render(str(currentOffset-player.climbAcc()), 1, (220, 0, 255))

        if not inPause and not inMenu and not isDead and not won:
            surface.blit(Ui_bg, (0, 0))
            surface.blit(score_display, (640, 107))
            surface.blit(Oxygen_display, (640, 200))
            surface.blit(oxyImage, (537, 252))
            surface.blit(Depth_display, (640, 377))

            # Lives display
            for i in range(0, player.livesAcc()):
                surface.blit(icon, (700-i*70, 500))

        nbFrame += 1
        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)


