from os import path
import pygame


class Block:
    """General block mother-class"""

    def __init__(self, posX, posY):
        self._posX = posX
        self._posY = posY
        self._bg = path.join("Assets", "Textures", "Background", "bg.png")


class Classic(Block):
    """Classic block daughter-class"""

    def __init__(self, posX, posY, colour):
        Block.__init__(self, posX, posY)
        self.__colour = colour
        self.__texturePath = path.join("Assets", "Textures", "Blocks", str(colour), "b_s.png")
        self.__hp = 1

    def hpAccess(self):
        return self.__hp

    def display(self, surface):

        if self.__hp > 0:
            image = pygame.image.load(self.__texturePath)
            surface.blit(image, (self._posX*64+26, self._posY*64+12))

        else:
            image = pygame.image.load(self._bg)
            surface.blit(image, (self._posX * 64 + 26, self._posY * 64 + 12))

    def hit(self, surface):

        self.__hp -= 1
        self.display(surface)


class Unbreakable(Block):
    """Unbreakable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY)
        self.__texturePath = path.join("Assets ", "Textures", "Blocks", "Unbreakable", "b_s.png")
        self.__hp = 5


class Solo(Block):
    """Not connectable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY)
        self.__texturePath = path.join("Assets ", "Textures", "Blocks", "Solo", "b_s.png")
        self.__hp = 1


class Delayed(Block):
    """Timeout block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY)
        self.__texturePath = path.join("Assets ", "Textures", "Blocks", "Delayed", "b_s.png")
        self.__hp = 1
        self.__timeout = 84    # number of image for fadeout
