import pygame
from os import path
#from character import *
import level


def storeScore(playerScore):
    # Opens file or creates it
    if path.isfile(path.join("Assets", "Score", "score.txt")):
        scoreFile = open(path.join("Assets", "Score", "score.txt"), "r+")
    else:
        scoreFile = open(path.join("Assets", "Score", "score.txt"), "w+")

    # Check if file is empty, if so, adds dummy scores
    scoreFile.seek(0)
    checkChar = scoreFile.read(1)
    scoreFile.seek(0)

    if not checkChar:
        for i in range(100, 400, 100):
            if i != 0:
                scoreFile.write(str(i) + "\n")
            else:
                scoreFile.write(str(1) + "\n")
        scoreFile.seek(0)

    # Get what is stored inside in an array.
    lines = scoreFile.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    # Convert array's items to integers, add playerScore and sort the array
    for i in range(len(lines)):
        lines[i] = int(lines[i])

    lines.append(playerScore)

    lines.sort(reverse=True)

    # Convert back to strings, in order to write in the file
    for i in range(len(lines)):
        lines[i] = str(lines[i])
        lines[i] = lines[i].strip()

    # Empties file and writes the array's items
    scoreFile.seek(0)
    scoreFile.truncate()
    scoreFile.seek(0)
    for item in lines:
        scoreFile.write(item + "\n")

    # Truncate file down to three lines
    scoreFile.seek(0)
    lineOffset = []
    offset = 0
    for line in scoreFile:
        lineOffset.append(offset)
        offset += len(line)

    scoreFile.seek(lineOffset[3] + 1)
    scoreFile.truncate()

    # Closes file
    scoreFile.close()


def readScore(surface):
    # Opens file and defines font
    scoreFile = open(path.join("Assets", "Score", "score.txt"), "r")
    FontUi = pygame.font.Font(path.join("Assets", "Misc", "police", "AOR_Improved.ttf"), 48)

    # Get scores from file
    lines = scoreFile.readlines()
    lines.sort(reverse=True)
    if len(lines) >= 3:
        dispQyt = 3
    else:
        dispQyt = len(lines)
    for i in range(dispQyt):
        lines[i] = lines[i].strip()
        ttd = str(i + 1)
        ttd += " : "
        ttd += lines[i]
        ttd.strip()
        scoreDisp = FontUi.render(ttd, 1, (220, 0, 255))
        surface.blit(scoreDisp, (i*240+30, 535))

    # Closes file
    scoreFile.close()


def mainMenu(surface, optionIM):

    bg = pygame.image.load(path.join("Assets", "Menu", "menu.png"))

    if optionIM == 1:
        playImg = pygame.image.load(path.join("Assets", "Buttons", "play_s.png"))
        quitImg = pygame.image.load(path.join("Assets", "Buttons", "quit_u.png"))
    elif optionIM == 2:
        playImg = pygame.image.load(path.join("Assets", "Buttons", "play_u.png"))
        quitImg = pygame.image.load(path.join("Assets", "Buttons", "quit_s.png"))

    surface.blit(bg, (0, 0))
    surface.blit(playImg, (310, 300))
    surface.blit(quitImg, (310, 400))
    readScore(surface)
    pygame.display.update()


def changeLvl(currentLvl, player):
    if currentLvl < 10:
        currentLvl += 1
        player.resetCoord(currentLvl)
        if currentLvl in [2, 7]:
            colors = 2
        else:
            colors = 4

        if currentLvl > 4:
            pillP = 2
            pillPL = 5
            pillMLE = 40
            soloP = 10
            unbreakableP = 10
            delayedP = 12
            lvl = level.generateLvl(colors, 155, 7, currentLvl, pillP, pillPL, pillMLE, soloP, unbreakableP, delayedP)
        else:
            lvl = level.generateLvl(colors, 80, 7, currentLvl)

        for row in lvl:
            for block in row:
                block.updCoText(lvl)

        won = False

        return lvl, currentLvl, won

    else:
        storeScore(player.scoreAcc())
        won = True
        lvl = [[]]
        return lvl, currentLvl, won


def restart(player):
    lvl, currentlvl, won = changeLvl(0, player)
    player.resetScore()
    return lvl, currentlvl, won









