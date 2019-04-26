import os
import pygame
from random import randint
import block


def generateLvl(colors, lines, width):    # This returns a 2D array [[color,color],[color,color],...]

    lvl = []
    for i in range(lines):
        line = []
        for j in range(width):
            newBlock = block.Classic(j, i, randint(1, colors))

            line.append(newBlock)
        lvl.append(line)

    return lvl


def deleteBlock(lvl, line, col):

    lvl[line][col] = 0
    return lvl


def displayLvLTxt(lvl):

    for element in lvl:
        print(element)


def pygRenderNxtLine(surface, currentLine, lvl):

    for element in lvl[currentLine]:
        element.display(surface)






