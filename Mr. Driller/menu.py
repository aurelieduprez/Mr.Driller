import pygame
from os import path
from character import *
from time import sleep
import level


def refreshScore(player):
    bestScore =[]
    score = player.scoreAcc()
    scoreFile = open(path.join("Assets", "Score", "score.txt"), "r+").readlines()
    scoreFile.append(score)
    ##scoreFile.split("[\\r\\n]+")
    print(scoreFile)
    for i in range(len(scoreFile)):
        scoreFile[i] = int(scoreFile[i])
    scoreFile.sort(reverse = True)
    for i in range(len(scoreFile)):
        scoreFile[i] = str(scoreFile[i])
    print(scoreFile)
    for k in range(3):
        print(k)
        bestScore.append(scoreFile[k])
    print(bestScore)


def displayScore(surface):
    ttd = ''
    FontUi = pygame.font.Font("Assets\Misc\police\Act_Of_Rejection.ttf", 36)
    scoreFile = open(path.join("Assets", "Score", "score.txt"), "r+").readlines()
    for i in range (3):
        ttd = "#" + str(i+1) + scoreFile[i]
        scoreDisplay = FontUi.render(ttd, 1, (220, 0, 0))
        surface.blit(scoreDisplay, (i*266, 520))



        
    






def mainMenu(surface, optionIM):
    bg = pygame.image.load(path.join("Assets", "Menu", "menu.png"))


    if optionIM == 1:
        playImg = pygame.image.load(path.join("Assets", "Buttons", "play_s.png"))
        quitImg = pygame.image.load(path.join("Assets", "Buttons", "quit_u.png"))
    elif optionIM == 2:
        playImg = pygame.image.load(path.join("Assets", "Buttons", "play_u.png"))
        quitImg = pygame.image.load(path.join("Assets", "Buttons", "quit_s.png"))

    displayScore(surface)
    surface.blit(bg, (0, 0))
    surface.blit(playImg, (310, 300))
    surface.blit(quitImg, (310, 400))







def changeLvl(currentLvl, player):
    currentLvl += 1
    player.resetCoord(currentLvl)
    if currentLvl in [2, 7]:
        colors = 2
    else:
        colors = 4

    if currentLvl > 5:
        pillP = 2
        pillPL = 5
        pillMLE = 40
        soloP = 10
        unbreakableP = 10
        delayedP = 12
        lvl = level.generateLvl(colors, 15, 7, currentLvl, pillP, pillPL, pillMLE, soloP, unbreakableP, delayedP)
    else:
        lvl = level.generateLvl(colors, 15, 7, currentLvl)

    for row in lvl:
        for block in row:
            block.updCoText(lvl)

    return lvl, currentLvl


def restart(player):
    lvl, currentlvl = changeLvl(0, player)
    player.resetScore()
    return lvl, currentlvl









