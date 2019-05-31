import pygame
from os import path


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


def refreshScore(newScore):

    content = open(path.join("Assets", "Score", "score.txt"), "r").read()    # Read file line by line
    print(content)
    score = str(content)
    score = score.split("#")   # Splits by "#"
    for i in range(len(score)):
        score[i] = int(score[i])
    score.append(newScore)  # adds score to list

    with open(path.join("Assets", "Score", "score.txt"), "w") as scoreFile:
        score.sort(reverse=True)    # sorts from biggest to smallest
        for i in range(len(score)):
            score[i] = str(score[i])
        line = "#".join(score)
        scoreFile.write(line)

    scoreFile.close()









