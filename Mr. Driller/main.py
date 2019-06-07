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
    icon = pygame.image.load(path.join("Assets", "Misc", "icon.png"))
    pygame.display.set_icon(icon)

    # Initializing useful variables
    currentBotLine = 8
    currentOffset = 0
    currentClimb = 0
    backDown = False

    blocksDisap = []
    level = []
    levelID = 1

    player = Character(3, 4, levelID, 0)    # Creates the player instance(posX, posY, bckgrnd, lives)

    # Custom Events
    EVCHGLVL = pygame.USEREVENT
    evChgLvl = pygame.event.Event(EVCHGLVL)
    EVTICSEC = pygame.USEREVENT + 1
    evTicSec = pygame.event.Event(EVTICSEC)
    EVTICOX2 = pygame.USEREVENT + 2
    evTicOx2 = pygame.event.Event(EVTICOX2)
    EVTICSIX = pygame.USEREVENT + 3
    evTicSix = pygame.event.Event(EVTICSIX)
    EVTICPLY = pygame.USEREVENT + 4
    evTicPly = pygame.event.Event(EVTICPLY)

    pygame.time.set_timer(EVTICSEC, 1050)
    pygame.time.set_timer(EVTICPLY, 850)
    pygame.time.set_timer(EVTICOX2, 750)
    pygame.time.set_timer(EVTICSIX, 175)

    # State of the Game
    inProgress = True
    inPause = False
    inMenu = True
    inGame = False
    isDead = False

    optionIM = 1
    optionID = 0
    hasToInit = True
    won = False
    ws = 0

    # Initializing Ui
    FontUi = pygame.font.Font(path.join("Assets", "Misc", "police", "Act_Of_Rejection.ttf"), 36)
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
            inGame = False
            pygame.mixer.music.stop()
            laugh = pygame.mixer.Sound(path.join("Assets", "Sounds", "laugh.wav"))
            laugh.set_volume(0.70)
            laugh.play(0)
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
                inProgress = False

            if event.type == EVCHGLVL:
                inGame = False
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

            if event.type == EVTICSEC:
                if inGame:
                    if levelID <= 4:
                        player.updateOxygen(1, surface, level)
                    # Delayed Blocks
                    for item in blocksDisap:
                        if level[item[0]][item[1]].hpAccess() > 0:
                            level[item[0]][item[1]].timeout()
                        elif level[item[0]][item[1]].hpAccess() == 0:
                            del(blocksDisap[blocksDisap.index(item)])

            if event.type == EVTICOX2:
                if levelID > 4 and inGame:
                    player.updateOxygen(1, surface, level)

            if event.type == EVTICPLY:
                if inGame:
                    player.NeedToIdle(surface)

            if event.type == EVTICSIX:
                if inGame:
                    player.Anim(surface)
                    render(surface, level, currentOffset)
                    player.display(surface)
                    for i in range(0, len(level), 1):
                        for element in level[i]:
                            # Delayed Blocks
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

            if event.type == KEYDOWN:       # Event handling

                if event.key == K_ESCAPE:
                    if not inPause and not inMenu and not isDead and not won or inGame:
                        # Changing context
                        inGame = False
                        inPause = True

                        option = 1
                        optionFile = str(option)
                        optionFile += ".png"
                        pauseImage = pygame.image.load(path.join("Assets", "Menu", optionFile))
                        surface.blit(pauseImage, (0, 0))

                    elif inPause:
                        # Changing context
                        inPause = False
                        render(surface, level, currentOffset)
                        player.display(surface)

                    elif isDead:
                        # Changing context
                        isDead = False
                        inMenu = True

                    elif won:
                        # Changing context
                        won = False
                        inMenu = True
                        music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                        pygame.mixer.music.play(-1, 0)

                if event.key in movKeys:    # Movement

                    if not inPause and not inMenu and not isDead and not won:
                        inGame = True
                        player.NeedToIdle(surface)
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

                        elif event.key == movKeys[0] and option > 1:
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
                        player.NeedToIdle(surface)
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
                            # Changing context
                            inPause = False
                            inMenu = True
                            mainMenu(surface, optionIM)
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                            pygame.mixer.music.play(-1, 0)

                    elif inMenu:
                        if optionIM == 1:
                            # Changing context
                            inMenu = False
                            hasToInit = False

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
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "Level1.wav"))
                            pygame.mixer.music.play(-1, 0)
                            surface.blit(splashLvl1, (0, 0))
                            pygame.display.update()
                            pygame.time.wait(3000)

                        elif optionID == 2:
                            inMenu = True
                            isDead = False
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                            pygame.mixer.music.play(-1, 0)

                    elif won:
                        if ws == 1:
                            ws = 2
                        elif ws == 3:
                            inMenu = True
                            won = False
                            music = pygame.mixer.music.load(path.join("Assets", "Music", "menu.wav"))
                            pygame.mixer.music.play(-1, 0)

        # Cleanup after a climb
        if backDown and player.climbAcc() < currentClimb:
            if currentClimb == 0:
                backDown = False
            player.backDownCleanup(surface)
        currentClimb = player.climbAcc()
        if player.climbAcc() > 0:
            backDown = True

        # Updating blocks when falling
        if inGame:
            player.fall(surface, level)
        if player.blocksFallenAcc() != currentOffset and inGame:
            currentOffset += 1
            currentBotLine += 1
            for i in range(0, len(level), 1):
                for element in level[i]:
                    element.updOffset(currentOffset)

        # Keeping oxygen, score and depth display U2D
        fileName = str(player.oxyAcc())
        fileName += ".png"
        oxyImage = pygame.image.load(path.join("Assets", "Misc", "oxyAnim", fileName))
        Oxygen_display = FontUi.render(str(player.oxyAcc()), 1, (220, 0, 255))

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

        pygame.display.update()
        fpsClock.tick(FPS)

    pygame.quit()


game(800, 600)
