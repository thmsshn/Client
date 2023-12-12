#from pygame import *
#import pyganim
#import os
#
#MONSTER_WIDTH = 32
#MONSTER_HEIGHT = 32
#MONSTER_COLOR = "#2110FF"
#
#
#class Monster(sprite.Sprite):
#    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
#        sprite.Sprite.__init__(self)
#        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
#        self.image.fill(Color(MONSTER_COLOR))
#        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
#        self.image.set_colorkey(Color(MONSTER_COLOR))
#        self.startX = x
#        self.startY = y
#        self.maxLengthLeft = maxLengthLeft
#        self.maxLengthUp = maxLengthUp
#        self.xvel = left
#        self.yvel = up
#
#    def update(self, platforms):
#        self.image.fill(Color(MONSTER_COLOR))
#
#        self.rect.y += self.yvel
#        self.rect.x += self.xvel
#
#        self.collide(platforms)
#
#        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
#            self.xvel = -self.xvel
#        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
#            self.yvel = -self.yvel
#
#    def collide(self, platforms):
#        for p in platforms:
#            if sprite.collide_rect(self, p) and self != p:
#                self.xvel = - self.xvel
#                self.yvel = - self.yvel