import pygame
import time
from os import path
from level import level
from time import sleep


class Character:        # Important : directions list : Up = 1; Right = 2; Down = 3; Left = 4
    """Character class"""

    def __init__(self, posX, posY, currentBotLine, surface, lives):

        # Position
        self.__posX = posX
        self.__posY = posY
        self.__blocksFallen = 0
        self.__climb = 0

        # Stats
        self.__oxygen = 100
        self.__lives = lives
        self.__score = 0

        # Textures
        self.__bg = path.join("Assets", "Textures", "Background", "bg.png")

        #Animation
        self.__IsMovingRight = False
        self.__IsMovingLeft = False
        self.__IsFalling = False
        self.__IsDrillingRight = False
        self.__IsDrillingLeft = False
        self.__IsDrillingRight_off = False
        self.__IsDrillingLeft_off = False
        self.__IsDrillingDown = False
        self.__IsReviving = False
        self.__IsIdling = True


        # Accessors
        self.__surface = surface

    def NeedToIdle(self,surface):
        self.__IsIdling = True
        self.Anim(surface)

    def IdlingAcc(self):
        return self.__IsIdling
    def blocksFallenAcc(self):
        return self.__blocksFallen

    def climbAcc(self):
        return self.__climb

    def oxyAcc(self):
        return self.__oxygen

    def scoreAcc(self):
        return self.__score

    # Animation

    def Anim(self,surface):

        if self.__IsIdling:
            if(self.__oxygen>20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_d_off.png")
                self.__IsIdling = True
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_d_off_o2.png")
                self.__IsIdling = True


        if self.__IsFalling:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_fall.png")
                self.__IsFalling = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_fall_o2.png")
                self.__IsFalling = False
                self.__IsIdling = False

        if self.__IsReviving:
            self.__texturePath = path.join("Assets", "Textures", "Character", "play_dead_y.png")
            self.__IsReviving = False
            self.__IsIdling = False


        if self.__IsMovingLeft:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_mov.png")
                self.__IsMovingLeft = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_mov_o2.png")
                self.__IsMovingLeft = False
                self.__IsIdling = False

        if self.__IsMovingRight:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_mov.png")
                self.__IsMovingRight = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_mov_o2.png")
                self.__IsMovingRight = False
                self.__IsIdling = False

        if self.__IsDrillingRight_off:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_off.png")
                self.__IsDrillingRight_off = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_off_o2.png")
                self.__IsDrillingRight_off = False
                self.__IsIdling = False

        if self.__IsDrillingLeft_off:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_off.png")
                self.__IsDrillingLeft_off = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_off_o2.png")
                self.__IsDrillingLeft_off = False
                self.__IsIdling = False

        if self.__IsDrillingRight:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_on.png")
                self.__IsDrillingRight = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_r_on_o2.png")
                self.__IsDrillingRight = False
                self.__IsIdling = False

        if self.__IsDrillingLeft:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_on.png")
                self.__IsDrillingLeft = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_l_on_o2.png")
                self.__IsDrillingLeft = False
                self.__IsIdling = False

        if self.__IsDrillingDown:
            if (self.__oxygen > 20):
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_d_on.png")
                self.__IsDrillingDown = False
                self.__IsIdling = False
            else:
                self.__texturePath = path.join("Assets", "Textures", "Character", "play_d_on_o2.png")
                self.__IsDrillingDown = False
                self.__IsIdling = False

        self.display(surface)
    # Logical Methods

    def AddScore(self, x):
        self.__score += x
        print("score", str(self.__score))
        return (self.__score)

    def move(self, surface, direction, level):

        # Right

        if direction == 2:
            self.__IsMovingRight = True

        if direction == 2 and self.__posX < len(level[0]) - 1\
                and level[self.__posY][self.__posX + 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX += 1
            self.display(surface)
            level[self.__posY][self.__posX-1].display(surface, self.__blocksFallen)

        # Right Pill
        elif direction == 2 and self.__posX < len(level[0]) - 1 and level[self.__posY][self.__posX + 1].typeAccess() == "pill" :
            level[self.__posY][self.__posX + 1].hit(surface, level, self)
            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX += 1
            self.display(surface)
            level[self.__posY][self.__posX - 1].display(surface, self.__blocksFallen)

        # Right Climb

        elif direction == 2 and self.__posX < len(level[0]) - 1\
                and level[self.__posY][self.__posX + 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX + 1].hpAccess() == 0 :

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX += 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)
            level[self.__posY][self.__posX - 1].display(surface, self.__blocksFallen)

        #Right Climb Pill

        elif direction == 2 and self.__posX < len(level[0]) - 1 \
                and level[self.__posY][self.__posX + 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX + 1].typeAccess() == "pill" :

            level[self.__posY - 1][self.__posX + 1].hit(surface, level, self)

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX += 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)
            level[self.__posY][self.__posX - 1].display(surface, self.__blocksFallen)

        # Left
        if direction == 4:
            self.__IsMovingLeft = True

        if direction == 4 and self.__posX > 0 \
                and level[self.__posY][self.__posX - 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX -= 1
            self.display(surface)
            level[self.__posY][self.__posX + 1].display(surface, self.__blocksFallen)



        # Left Pill
        elif direction == 4 and self.__posX > 0 - 1 and level[self.__posY][self.__posX - 1].typeAccess() == "pill" :
            level[self.__posY][self.__posX - 1].hit(surface, level, self)
            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX -= 1
            self.display(surface)
            level[self.__posY][self.__posX + 1].display(surface, self.__blocksFallen)


        # Left Climb

        elif direction == 4 and self.__posX > 0 \
            and level[self.__posY][self.__posX - 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX - 1].hpAccess() == 0:

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX -= 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)
            level[self.__posY][self.__posX + 1].display(surface, self.__blocksFallen)

        #Left Climb Pill

        elif direction == 4 and self.__posX > 0 \
                and level[self.__posY][self.__posX - 1].hpAccess() != 0 \
                and level[self.__posY - 1][self.__posX].hpAccess() == 0 \
                and level[self.__posY - 1][self.__posX - 1].typeAccess() == "pill" :

            level[self.__posY - 1][self.__posX - 1].hit(surface, level, self)

            level[self.__posY][self.__posX].display(surface, self.__blocksFallen)
            self.__posX -= 1
            self.__posY -= 1
            self.__climb += 1
            self.display(surface)
            level[self.__posY][self.__posX + 1].display(surface, self.__blocksFallen)

    def breakBlock(self, surface, direction, level, currentBotLine):

        # Right

        if direction == 2:
            self.__IsDrillingRight_off = True

            if self.__posX < len(level[0])-1 \
                and level[self.__posY][self. __posX + 1].hpAccess() > 0\
                and level[self.__posY][self.__posX + 1].typeAccess() != "pill":
                self.__IsDrillingRight = True
                level[self.__posY][self. __posX+1].hit(surface, level, self)

        # Down

        elif direction == 3 \
                and self.__posY < currentBotLine \
                and level[self.__posY + 1][self.__posX].hpAccess() > 0 \
                and level[self.__posY + 1][self.__posX].typeAccess() != "pill":
                self.__IsDrillingDown = True
                level[self.__posY+1][self. __posX].hit(surface, level, self)

        # Left

        elif direction == 4 :
            self.__IsDrillingLeft_off = True
            if self.__posX > 0 \
                and level[self.__posY][self. __posX - 1].hpAccess() > 0 \
                and level[self.__posY][self.__posX - 1].typeAccess() != "pill" :
                self.__IsDrillingLeft = True
                level[self.__posY][self. __posX-1].hit(surface, level, self)

    def fall(self, surface, level):

        if self.__posY < len(level)-2 and level[self.__posY+1][self.__posX].hpAccess() == 0\
                or level[self.__posY + 1][self.__posX].typeAccess() == "pill":

            if self.__climb == 0:
                if level[self.__posY + 1][self.__posX].typeAccess() == "pill":
                    level[self.__posY + 1][self.__posX].hit(surface, level, self)

                self.__blocksFallen += 1
                self.__posY += 1
                self.__IsFalling = True

            else:
                if level[self.__posY + 1][self.__posX].typeAccess() == "pill":
                    level[self.__posY + 1][self.__posX].hit(surface, level, self)

                self.__climb -= 1
                self.__posY += 1

            return self.__blocksFallen

    def revive(self, surface):
        if self.__lives == 0:
            print("dead")   # End
        else:
            self.__IsReviving = True
            self.__oxygen = 100
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
            self.__oxygen = 100

            self.__oxygen = 100

    def updateOxygen(self, type, surface):
        if type == 1:
            self.__oxygen -= 1
        elif type == 2:
            self.__oxygen -= 20
        elif type == 3:
            if self.__oxygen <= 70:
                self.__oxygen += 30
            else:
                self.__oxygen = 100

        if self.__oxygen <= 0:
            self.revive(surface)

    # Graphical Methods

    def display(self, surface):

        image = pygame.image.load(self.__texturePath)
        surface.blit(image, (self.__posX * 64 + 26, (self.__posY * 64 + 12) - self.__blocksFallen * 64))

    def backDownCleanup(self, surface):
        image = pygame.image.load(self.__bg)
        surface.blit(image, (self.__posX * 64 + 26, (self.__posY * 64 + 12) - self.__blocksFallen * 64 - 64))
        self.display(surface)

