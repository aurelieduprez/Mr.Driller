import pygame
from random import randint


def generateLvl(colors, lines, width):    # This returns a 3D array [[[color, state]

    lvl = []
    for i in range(lines):
        line = []
        for j in range(width):
            block = randint(1, colors)

            line.append(block)

        lvl.append(line)

    return lvl


def deleteBlock(lvl, line, col):

    lvl[line][col] = 0
    return lvl


def displayLvLTxt(lvl):

    for element in lvl:
        print(element)


def pygameRender(surface, lvl):

    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    surface.fill(color)

