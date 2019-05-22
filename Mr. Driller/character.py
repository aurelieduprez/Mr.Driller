from os import path
import pygame
from level import render,level


class Character:        # Important : directions list : Up = 1; Right = 2; Down = 3; Left = 4
    """Character class"""

    def __init__(self, posX, posY, currentBotLine,Lives):
        self.__Lives = Lives
        self.__posX = posX
        self.__posY = posY
        self.__blocksFallen = 0
        self.__climb = 0
        self.__oxygen = 100
        self.__texturePath = path.join("Assets", "Textures", "Character", "testpink.png")

    def blocksFallenAcc(self):
        return self.__blocksFallen

    def Revive(self,surface):
        if self.__Lives == 0:
            print("dead") #à replacer par un endscreen
        else:
            print('being revive')
            #add 100% oxygen
            self.__Lives -=1
            for i in range(-2,1):
                if (self.__posX + 1)!= 7:
                    if(level[self.__posY+i][self.__posX + 1].hpAccess() != 0):
                        level[self.__posY+i][self.__posX + 1].hit(surface,1)
                if (self.__posX - 1)!= -1:
                    if(level[self.__posY+i][self.__posX - 1].hpAccess() != 0):
                        level[self.__posY+i][self.__posX - 1].hit(surface,1)
                if (level[self.__posY + i][self.__posX].hpAccess() != 0):
                    level[self.__posY + i][self.__posX].hit(surface,1)


    def display(self, surface):

        image = pygame.image.load(self.__texturePath)
        surface.blit(image, (self.__posX * 64 + 26, (self.__posY * 64 + 12) - self.__blocksFallen * 64))

    def move(self, surface, direction, level):

        if direction == 2 and self.__posX < len(level[0])-1 and self.__posX < len(level[0])-1 \
        and level[self.__posY][self. __posX+1].hpAccess() == 0:        # Right
            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX += 1
            self.display(surface)

        elif direction == 3 and self.__posX > 0 \
        and level[self.__posY][self. __posX-1].hpAccess() == 0:                     # Left
            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX -= 1
            self.display(surface)

    def breakBlock(self, surface, direction, level, currentBotLine):

        if direction == 2 \
                and self.__posX < len(level[0])-1 \
                and level[self.__posY][self. __posX+1].hpAccess() > 0:

            print("tried to hit", self.__posY-self.blocksFallenAcc(), self.__posX+1)
            level[self.__posY][self. __posX+1].hit(surface)             # Right

        elif direction == 3 \
                and self.__posY < currentBotLine \
                and level[self.__posY+1][self. __posX].hpAccess() > 0:
            level[self.__posY+1][self. __posX].hit(surface)             # Down

        elif direction == 4 \
                and self.__posX > 0 \
                and level[self.__posY][self. __posX-1].hpAccess() > 0:
            level[self.__posY][self. __posX-1].hit(surface)             # Left

    def fall(self, surface, level):

        if self.__posY < len(level)-2 and level[self.__posY+1][self.__posX].hpAccess() == 0:
            self.__blocksFallen += 1
            self.__posY += 1

            return self.__blocksFallen

    def updateOxygen(self,type): #type 1 : perd 1 oxygen par seconde, 2 : -20 oxygen (bloc unbreakable), 3 : + X oxygen (capsule)
        if type == 1 :
            self.__oxygen = self.__oxygen - 1
        elif type == 2 :
            self.__oxygen = self.__oxygen - 20
        elif type == 3:
            self.__oxygen = self.__oxygen + 50
