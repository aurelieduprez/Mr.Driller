from os import path
import pygame


class Block:
    """General block mother-class"""

    def __init__(self, posX, posY, forceHP):
        self._posX = posX
        self._posY = posY
        self._currOffset = 0

        self._hp = forceHP

        self._texturePath = path.join("Assets", "Textures", "Blocks", "Neutral", "b_s.png")
        self._bg = path.join("Assets", "Textures", "Background", "bg.png")

    def hpAccess(self):
        return self._hp

    def updOffset(self, currentOffset):
        self._currOffset = currentOffset

    def display(self, surface, forceBG=0, currentOffset=0):

        if self._hp == 0 or forceBG == 1:
            image = pygame.image.load(self._bg)
            surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))

        elif self._hp > 0:
            image = pygame.image.load(self._texturePath)
            surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))

    def hit(self, surface):

        self._hp -= 1
        print("-1hp")
        self.display(surface, 0, self._currOffset)


class Classic(Block):
    """Classic block daughter-class"""

    def __init__(self, posX, posY, colour, forceHP):
        Block.__init__(self, posX, posY, forceHP)
        self.__colour = colour
        self._texturePath = path.join("Assets", "Textures", "Blocks", str(colour), "b_s.png")


class Unbreakable(Block):
    """Unbreakable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 5)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Unbreakable", "b_s.png")


class Solo(Block):
    """Not connectable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY,1)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Solo", "b_s.png")


class Delayed(Block):
    """Timeout block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY,1)
        self.__texturePath = path.join("Assets", "Textures", "Blocks", "Delayed", "b_s.png")
        self.__timeout = 84    # number of image for fadeout

class Pill(Block):


    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY,1)
        self.__texturePath = path.join("Assets", "Textures", "Blocks", "Pill", "pill.png")
