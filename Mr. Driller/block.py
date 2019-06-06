from connectCorrect import *
from os import path
import pygame
from menu import *


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
        self._bg = path.join("Assets", "Textures", "Background", "bg_1.png")

    # Accessors

    def hpAccess(self):
        return self._hp

    def ColorAccess(self):
        return self._colors

    def typeAccess(self):
        return self._blockType

    # Logical Method

    def changeBG(self, bg):
        file = "bg_"
        file += str(bg)
        file += ".png"
        self._bg = path.join("Assets", "Textures", "Background", file)

    def updOffset(self, currentOffset):
        self._currOffset = currentOffset

    def hit(self, surface, level, player, nochain=0, instakill=0, delayedTimeout=0):
        if instakill:
            self._hp = 0

        if self._blockType == "unbreakable":
            self._hp -= 1
            self.updTexture()
            if self.hpAccess() == 0:
                self._brkSound.play()
                player.updateOxygen(2, surface, level)
                player.AddScore(10)
            else:
                self._hitSound.play()

        elif self._blockType == "pill":
            player.updateOxygen(3, surface, level)
            player.AddScore(20)
            self._hp -= 1

        elif self._blockType == "delayed":
            if not self.idAcc():
                player.AddScore(10)
            self._isDisappearing = True
            self.updTexture()

        elif self._blockType == "end":
            self.changeLvl()
            refreshScore(player)
            self._hp -= 1

        else:
            player.AddScore(10)
            self._hp -= 1

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

            if self._posX < len(level[0]) - 1 and level[self._posY][self._posX + 1].hpAccess() != 0 \
                    and level[self._posY][self._posX + 1].typeAccess() == "classic":

                if level[self._posY][self._posX + 1].ColorAccess() == self._colors:
                    level[self._posY][self._posX + 1].hit(surface, level, player)

            if level[self._posY][self._posX - 1].hpAccess() != 0 and self._posX > 0 \
                    and level[self._posY][self._posX - 1].typeAccess() == "classic":

                if level[self._posY][self._posX - 1].ColorAccess() == self._colors:
                    level[self._posY][self._posX - 1].hit(surface, level, player)

        self.display(surface, self._currOffset)

    # Graphical Methods

    def updCoText(self, level):

        topLeft = False
        topRight = False
        botLeft = False
        botRight = False
        total = 0

        if self._chain_reaction == 1 and self._blockType == "classic":

            # Bottom
            if level[self._posY + 1][self._posX].hpAccess() != 0 \
                    and level[self._posY + 1][self._posX].typeAccess() == "classic":

                if level[self._posY + 1][self._posX].ColorAccess() == self._colors:
                    total += 32

                    if self._posX > 0 and not botLeft:
                        if level[self._posY + 1][self._posX - 1].typeAccess() == "classic":
                            if level[self._posY + 1][self._posX - 1].ColorAccess() == self._colors:
                                botLeft = True

                    if self._posX < len(level[0]) - 1 and not botRight:
                        if level[self._posY + 1][self._posX + 1].typeAccess() == "classic":
                            if level[self._posY + 1][self._posX + 1].ColorAccess() == self._colors:
                                botRight = True

            # Top
            if level[self._posY - 1][self._posX].hpAccess() != 0 \
                    and level[self._posY - 1][self._posX].typeAccess() == "classic":

                if level[self._posY - 1][self._posX].ColorAccess() == self._colors:
                    total += 128

                    if self._posX > 0 and not topLeft:
                        if level[self._posY - 1][self._posX - 1].typeAccess() == "classic":
                            if level[self._posY - 1][self._posX - 1].ColorAccess() == self._colors:
                                topLeft = True

                    if self._posX < len(level[0]) - 1 and not botRight:
                        if level[self._posY - 1][self._posX + 1].typeAccess() == "classic":
                            if level[self._posY - 1][self._posX + 1].ColorAccess() == self._colors:
                                topRight = True

            # Right
            if self._posX < len(level[0]) - 1 and level[self._posY][self._posX + 1].hpAccess() != 0 \
                    and level[self._posY][self._posX + 1].typeAccess() == "classic":

                if level[self._posY][self._posX + 1].ColorAccess() == self._colors:
                    total += 64

                    if not topRight:
                        if level[self._posY - 1][self._posX + 1].typeAccess() == "classic":
                            if level[self._posY - 1][self._posX + 1].ColorAccess() == self._colors:
                                topRight = True

                    if not botRight:
                        if level[self._posY + 1][self._posX + 1].typeAccess() == "classic":
                            if level[self._posY + 1][self._posX + 1].ColorAccess() == self._colors:
                                botRight = True

            # Left
            if level[self._posY][self._posX - 1].hpAccess() != 0 and self._posX > 0 \
                    and level[self._posY][self._posX - 1].typeAccess() == "classic":

                if level[self._posY][self._posX - 1].ColorAccess() == self._colors:
                    total += 16

                    if not topLeft:
                        if level[self._posY - 1][self._posX - 1].typeAccess() == "classic":
                            if level[self._posY - 1][self._posX - 1].ColorAccess() == self._colors:
                                topLeft = True

                    if not botLeft:
                        if level[self._posY + 1][self._posX - 1].typeAccess() == "classic":
                            if level[self._posY + 1][self._posX - 1].ColorAccess() == self._colors:
                                botLeft = True

            if botLeft:
                total += 1
            if botRight:
                total += 2
            if topLeft:
                total += 4
            if topRight:
                total += 8

            # Override for BotTop and Left-Right

            # Left-Right

            if 0 < self._posX < len(level[0]) - 1:
                valid = True
                if hasattr(level[self._posY - 1][self._posX], "_colors"):
                    if level[self._posY - 1][self._posX].ColorAccess() == self._colors:
                        valid = False

                if hasattr(level[self._posY + 1][self._posX], "_colors"):
                    if level[self._posY + 1][self._posX].ColorAccess() == self._colors:
                        valid = False

                if valid:
                    if level[self._posY][self._posX - 1].hpAccess() != 0 \
                            and level[self._posY][self._posX - 1].typeAccess() == "classic" \
                            and level[self._posY][self._posX + 1].hpAccess() != 0 \
                            and level[self._posY][self._posX + 1].typeAccess() == "classic":

                        if level[self._posY][self._posX - 1].ColorAccess() == self._colors \
                                and level[self._posY][self._posX + 1].ColorAccess() == self._colors:
                            total = 64 + 16

            # Top-Bottom
            if 0 < self._posX < len(level[0]) - 1:

                validTB = True
                if hasattr(level[self._posY][self._posX-1], "_colors"):
                    if level[self._posY][self._posX-1].ColorAccess() == self._colors:
                        validTB = False

                if hasattr(level[self._posY][self._posX+1], "_colors"):
                    if level[self._posY][self._posX+1].ColorAccess() == self._colors:
                        validTB = False

                if validTB:
                    if level[self._posY - 1][self._posX].hpAccess() != 0 \
                            and level[self._posY - 1][self._posX].typeAccess() == "classic" \
                            and level[self._posY + 1][self._posX].hpAccess() != 0 \
                            and level[self._posY + 1][self._posX].typeAccess() == "classic":

                        if level[self._posY - 1][self._posX].ColorAccess() == self._colors \
                                and level[self._posY + 1][self._posX].ColorAccess() == self._colors:
                            total = 128 + 32

            total = correct(total)

            self._texturePath = path.join("Assets", "Textures", "Blocks", str(self._colors), (str(total) + ".png"))

    def display(self, surface, currentOffset=0):

        image = pygame.image.load(self._bg)
        surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))

        if self._hp > 0:
            image = pygame.image.load(self._texturePath)
            surface.blit(image, (self._posX * 64 + 26, (self._posY * 64 + 12) - currentOffset*64))


class Classic(Block):
    """Classic block daughter-class"""

    def __init__(self, posX, posY, colors, forceHP):
        Block.__init__(self, posX, posY, forceHP, 1, colors)
        self.__colors = colors
        self._texturePath = path.join("Assets", "Textures", "Blocks", str(colors), "0.png")
        self._blockType = "classic"


class Unbreakable(Block):
    """Unbreakable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 5, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Unbreakable", "5.png")
        self._blockType = "unbreakable"
        self._brkSound = pygame.mixer.Sound(path.join("Assets", "Sounds", "unbreakable.wav"))
        self._hitSound = pygame.mixer.Sound(path.join("Assets", "Sounds", "tac.wav"))

    def updTexture(self):
        name = str(self.hpAccess())
        name += ".png"
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Unbreakable", name)


class Solo(Block):
    """Not connectable block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Solo", "b_s.png")
        self._blockType = "solo"


class Delayed(Block):
    """Timeout block daughter-class"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 5, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Delayed", "0.png")
        self._isDisappearing = False
        self._blockType = "delayed"
        self.__seconds = 2    # number of image for fadeout

    def idAcc(self):
        return self._isDisappearing

    def posAcc(self):
        return self._posY, self._posX

    def updTexture(self):
        if self._isDisappearing:
            if self.hpAccess() > 0:
                textName = str(self.__seconds)
                textName += ".png"
                self._texturePath = path.join("Assets", "Textures", "Blocks", "Delayed", textName)

    def timeout(self, surface, currentOffset):

        if self._isDisappearing:
            self.__seconds -= 1
            self.updTexture()
            self.display(surface)

        if self.__seconds == 0:
            self._hp = 0


class Pill(Block):
    """Oxygen Pill"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Pill", "pill_1.png")
        self._blockType = "pill"

    def changeBG(self, bg):
        text = "pill_"
        text += str(bg)
        text += ".png"
        self._texturePath = path.join("Assets", "Textures", "Blocks", "Pill", text)
        file = "bg_"
        file += str(bg)
        file += ".png"
        self._bg = path.join("Assets", "Textures", "Background", file)


class End(Block):
    """End block"""

    def __init__(self, posX, posY):
        Block.__init__(self, posX, posY, 1, 0)
        self._texturePath = path.join("Assets", "Textures", "Blocks", "End", "b_s.png")
        self._blockType = "end"
        self._nextLvl = False

    def nextLvlAcc(self):
        return self._nextLvl

    def changeLvl(self):
        evChgLvl = pygame.event.Event(pygame.USEREVENT, attr1="evChgLvl")
        pygame.event.post(evChgLvl)



