from os import path
import pygame
import ui


class Block:
    """General block mother-class"""

    def __init__(self, posX, posY, forceHP, chain_reaction, colors=0):

        # Position
        self._posX = posX
        self._posY = posY
        self._currOffset = 0

        # Stats
        self._hp = forceHP
        self._blockType = "neutral"

        # Chain Reaction
        if(chain_reaction):
            self._colors = colors
        self._chain_reaction = chain_reaction

        # Textures
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Neutral", "b_s.png")
        self._bg = path.join("Assets", "Textures", "Background", "bg.png")

    # Accessors

    def hpAccess(self):
        return self._hp

    def ColorAccess(self):
        return self._colors

    def typeAccess(self):
        return self._blockType

    # Logical Method

    def updOffset(self, currentOffset):
        self._currOffset = currentOffset

    def hit(self, surface, level, player, nochain=0, instakill=0):
        if instakill:
            self._hp = 0

        else:
            self._hp -= 1

        if self._blockType == "unbreakable" and self._hp == 0:
            player.updateOxygen(2)  # Ici il faut changer la fonction pour qu'on arrive à la déclencher
            ui._score += 10
            print("score:",self._score)

        elif self._blockType == "pill" and self._hp == 0:
            player.updateOxygen(3)
            ui._score += 100
            print("score:", self._score)

        # Chain reaction
        if self._chain_reaction == 1 and nochain == 0 and self._blockType == "classic":

            if level[self._posY + 1][self._posX].hpAccess() != 0 \
                    and level[self._posY + 1][self._posX].typeAccess() == "classic":

                if level[self._posY + 1][self._posX].ColorAccess() == self._colors:
                    level[self._posY + 1][self._posX].hit(surface, level, player)

            if level[self._posY - 1][self._posX].hpAccess() != 0 \
                    and level[self._posY - 1][self._posX].typeAccess() == "classic":

                if level[self._posY - 1][self._posX].ColorAccess() == self._colors:
                    level[self._posY - 1][self._posX].hit(surface, level, player)

            if self._posX < len(level[0]) - 1 and self._posX < len(level[0]) - 1 and level[self._posY][
                self._posX + 1].hpAccess() != 0 \
                    and level[self._posY][self._posX + 1].typeAccess() == "classic":
                if level[self._posY][self._posX + 1].ColorAccess() == self._colors:
                    level[self._posY][self._posX + 1].hit(surface, level, player)

            if level[self._posY][self._posX - 1].hpAccess() != 0 and self._posX > 0 \
                    and level[self._posY][self._posX - 1].typeAccess() == "classic":
                if level[self._posY][self._posX - 1].ColorAccess() == self._colors:
                    level[self._posY][self._posX - 1].hit(surface, level, player)

        self.display(surface, 0, self._currOffset)

    # Graphical Method

    def display(self, surface, forceBG=0, currentOffset=0):

        if self._hp == 0 or forceBG == 1:
            image = pygame.image.load(self._bg)
            surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))

        elif self._hp > 0:
            image = pygame.image.load(self._texturePath)
            surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))


class Classic(Block):
    """Classic block daughter-class"""

    def __init__(self, posX, posY, colors, forceHP):
        Block.__init__(self, posX, posY, forceHP, 1, colors)
        self.__colors = colors
        self._texturePath = path.join("Assets", "Textures", "Blocks", str(colors), "b_s.png")
        self._blockType = "classic"


class Unbreakable(Block):
    """Unbreakable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 5, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Unbreakable", "b_s.png")
        self._blockType = "unbreakable"


class Solo(Block):
    """Not connectable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Solo", "b_s.png")
        self._blockType = "solo"


class Delayed(Block):
    """Timeout block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self.__texturePath = path.join("Assets", "Textures", "Blocks", "Delayed", "b_s.png")
        self._blockType = "delayed"
        self.__timeout = 84    # number of image for fadeout


class Pill(Block):
    """Oxygen Pill"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Pill", "pill.png")
        self._blockType = "pill"

class End(Block):
    """End block"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "End", "b_s.png")
        self._blockType = "end"

