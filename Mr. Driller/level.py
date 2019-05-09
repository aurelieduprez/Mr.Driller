import os
import pygame
from random import randint
import block


def generateLvl(colors, lines, width):    # This returns a 2D array of blocks [Y][X]

    lvl = []

    for i in range(lines+5):
        line = []

        if i in range(5):   # Override for first 5 lines -> generates empty blocks
            for j in range(width):
                newBlock = block.Classic(j, i, 1, 1)
                line.append(newBlock)

        else:
            for j in range(width):
                newBlock = block.Classic(j, i, randint(1, colors), 0)
                line.append(newBlock)

        lvl.append(line)

    return lvl


def pygRenderNxtLine(surface, currentLine, lvl):

    for element in lvl[currentLine]:
        element.display(surface)


def render(surface, level, currBotline, currOffset):

    # init
    if currOffset == 0:
        for i in range(currOffset, currBotline+1, 1):
            for element in level[i]:
                element.display(surface)

    # scroll up
    else:
        for i in range(currOffset, currOffset+9, 1):
            for element in level[i]:
                element.display(surface, 0, currOffset)







