import pygame
from os import path
from level import level


class Character:        # Important : directions list : Up = 1; Right = 2; Down = 3; Left = 4
    """Character class"""

    def __init__(self, posX, posY, currentBotLine, lives):

        # Position
        self.__posX = posX
        self.__posY = posY
        self.__blocksFallen = 0
        self.__climb = 0

        # Stats
        self.__oxygen = 100
        self.__lives = lives

        # Textures
        self.__bg = path.join("Assets", "Textures", "Background", "bg.png")
        self.__texturePath = path.join("Assets", "Textures", "Character", "testpink.png")

    # Accessors

    def blocksFallenAcc(self):
        return self.__blocksFallen

    def climbAcc(self):
        return self.__climb

    def oxyAcc(self):
        return self.__oxygen

    # Logical Methods

    def move(self, surface, direction, level):

        # Right

        if direction == 2 and self.__posX < len(level[0]) - 1 and self.__posX < len(level[0]) - 1 \
                and level[self.__posY][self.__posX + 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX += 1
            self.display(surface)

        # Right Climb

        elif direction == 2 and self.__posX < len(level[0]) - 1 and self.__posX < len(level[0]) - 1 \
                and level[self.__posY][self.__posX + 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX + 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX += 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)

        # Left

        elif direction == 3 and self.__posX > 0 \
                and level[self.__posY][self.__posX - 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX -= 1
            self.display(surface)

        # Left Climb

        elif direction == 3 and self.__posX > 0 \
            and level[self.__posY][self.__posX - 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX - 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, 0, self.__blocksFallen)
            self.__posX -= 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)

    def breakBlock(self, surface, direction, level, currentBotLine):

        # Right

        if direction == 2 \
                and self.__posX < len(level[0])-1 \
                and level[self.__posY][self. __posX+1].hpAccess() > 0:
            level[self.__posY][self. __posX+1].hit(surface, level, self)

        # Down

        elif direction == 3 \
                and self.__posY < currentBotLine \
                and level[self.__posY+1][self. __posX].hpAccess() > 0:
            level[self.__posY+1][self. __posX].hit(surface, level, self)

        # Left

        elif direction == 4 \
                and self.__posX > 0 \
                and level[self.__posY][self. __posX-1].hpAccess() > 0:
            level[self.__posY][self. __posX-1].hit(surface, level, self)

    def fall(self, surface, level):

        if self.__posY < len(level)-2 and level[self.__posY+1][self.__posX].hpAccess() == 0:
            if self.__climb == 0:
                self.__blocksFallen += 1
                self.__posY += 1
            else:
                self.__climb -= 1
                self.__posY += 1
            return self.__blocksFallen

    def revive(self, surface):
        if self.__lives == 0:
            print("dead")   # End
        else:
            print("being revived")
            # Sets 100% oxygen
            self.__lives -= 1
            for i in range(-2, 1):
                if (self.__posX + 1) != 7:
                    if level[self.__posY + i][self.__posX + 1].hpAccess() != 0:
                        level[self.__posY+i][self.__posX + 1].hit(surface, level, self, 1, 1)
                if (self.__posX - 1) != -1:
                    if level[self.__posY+i][self.__posX - 1].hpAccess() != 0:
                        level[self.__posY+i][self.__posX - 1].hit(surface, level, self, 1, 1)
                if level[self.__posY + i][self.__posX].hpAccess() != 0:
                    level[self.__posY + i][self.__posX].hit(surface, level, self, 1, 1)

    def updateOxygen(self, type):    # 1 : -1 oxygen/sec, 2 : -20 oxygen (bloc unbreakable), 3 : + X oxygen (pill)
        if type == 1:
            self.__oxygen -= 1
        elif type == 2:
            self.__oxygen -= 20
        elif type == 3:
            self.__oxygen += 30

    # Graphical Methods

    def display(self, surface):

        image = pygame.image.load(self.__texturePath)
        surface.blit(image, (self.__posX * 64 + 26, (self.__posY * 64 + 12) - self.__blocksFallen * 64))

    def backDownCleanup(self, surface):
        image = pygame.image.load(self.__bg)
        surface.blit(image, (self.__posX * 64 + 26, (self.__posY * 64 + 12) - self.__blocksFallen * 64 - 64))
        self.display(surface)

