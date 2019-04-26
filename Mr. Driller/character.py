from os import path
import pygame


class Character:        # Important : directions list : Up = 1; Right = 2; Down = 3; Left = 4
    """Character class"""

    def __init__(self, posX, posY):
        self.__posX = posX
        self.__posY = posY
        self.__texturePath = path.join("Assets", "Textures", "Character", "testpink.png")

    def display(self, surface):

        image = pygame.image.load(self.__texturePath)
        surface.blit(image, (self.__posX * 64 + 26, self.__posY * 64 + 12))

    def move(self, surface, direction, level):

        if direction == 1 and self.__posY > 0:                         # Up
            level[self.__posY][self.__posX].display(surface)
            self.__posY -= 1
            self.display(surface)

        elif direction == 2 and self.__posX < len(level[0])-1:        # Right
            level[self.__posY][self.__posX].display(surface)
            self.__posX += 1
            self.display(surface)

        elif direction == 3 and self.__posX > 0:                      # Left
            level[self.__posY][self.__posX].display(surface)
            self.__posX -= 1
            self.display(surface)

    def breakBlock(self, surface, direction, level):

        if direction == 1 \
                and self.__posY > 0 \
                and level[self.__posY-1][self. __posX].hpAccess() > 0:
            level[self.__posY-1][self. __posX].hit(surface)             # Up

        elif direction == 2 \
                and self.__posX < len(level[0])-1 \
                and level[self.__posY][self. __posX+1].hpAccess() > 0:
            level[self.__posY][self. __posX+1].hit(surface)             # Right

        elif direction == 3 \
                and self.__posY < len(level)-1 \
                and level[self.__posY+1][self. __posX].hpAccess() > 0:
            level[self.__posY+1][self. __posX].hit(surface)             # Down

        elif direction == 4 \
                and self.__posX > 0 \
                and level[self.__posY][self. __posX-1].hpAccess() > 0:
            level[self.__posY][self. __posX-1].hit(surface)             # Left

