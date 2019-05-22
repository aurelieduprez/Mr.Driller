import os
import pygame
from random import randint
import block

level = []
def generateLvl(colors, lines, width):    # This returns a 2D array of blocks [Y][X]

    global level

    for i in range(lines+5):
        line = []

        if i in range(5):   # Override for first 5 lines -> generates empty blocks
            for j in range(width):
                newBlock = block.Classic(j, i, 1, 0)
                line.append(newBlock)

        else:
            for j in range(width):
                x = randint(0,1)
                if(x == 1):
                    newBlock = block.Unbreakable(j, i)
                else:
                    newBlock = block.Pill(j, i)
                line.append(newBlock)

        level.append(line)

    return level


def render(surface, level, currOffset):

    # init
    if currOffset == 0:
        for i in range(currOffset, currOffset + 9, 1):
            for element in level[i]:
                element.display(surface)

    # scroll up
    else:
        for i in range(currOffset, currOffset+9, 1):
            for element in level[i]:
                element.display(surface, 0, currOffset)







