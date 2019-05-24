
import pygame
from character import *
from level import *
from os import name
from eventHandling import *

class Ui:



    def __init__(self, score=0):

        self._score = score

    def AddScore(self,x):
        self._score += x
        print("score"+str(self._score))


