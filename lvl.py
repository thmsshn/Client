from pygame import *
import os
import pyganim
from monsters import *

PLATFORM_WIDTH = 64
PLATFORM_HEIGHT = 64
PLATFORM_COLOR = "#3d6634"


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("blocks/derevo1.png")
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class BlockDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks/ship1.png")


class BlockTeleport(Platform):
    def __init__(self, x, y, goX, goY):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks/tp2.png")
        self.goX = goX
        self.goY = goY


class Door(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("blocks/door.png")



    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
