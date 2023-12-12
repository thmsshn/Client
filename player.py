import scipy. interpolate
from lvl import *
import pygame
from pygame import sprite, Surface, Color, Rect
from main import *
import pyganim
import os
from monsters import *
import lvl


walkRight = [pygame.image.load('sprite/право1.png'), pygame.image.load('sprite/право2.png'),
             pygame.image.load('sprite/право3.png'),pygame.image.load('sprite/право4.png'),
             pygame.image.load('sprite/право5.png'),pygame.image.load('sprite/право6.png'),
             pygame.image.load('sprite/право7.png'),pygame.image.load('sprite/право8.png')]

walkLeft = [pygame.image.load('sprite/лево1.png'), pygame.image.load('sprite/лево2.png'),
            pygame.image.load('sprite/лево3.png'),pygame.image.load('sprite/лево4.png'),
            pygame.image.load('sprite/лево5.png'),pygame.image.load('sprite/лево6.png'),
            pygame.image.load('sprite/лево7.png'),pygame.image.load('sprite/лево8.png')]
charimageLeft = pygame.image.load('sprite/лево1.png')
charimageRight = pygame.image.load('sprite/право1.png')
MOVE_SPEED = 3
MOVE_EXTRA_SPEED = 2.5
WIDTH = 38
HEIGHT = 48
COLOR = "#00ffffff"
JUMP_POWER = 10
JUMP_EXTRA_POWER = 1
GRAVITY = 0.35
left = False
right = False
animCount = 0




class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.winner = False
        self.xvel = 0
        self.startX = x
        self.startY = y
        self.yvel = 0
        self.onGround = False
        self.image = charimageRight
        #self.image.fill(COLOR)
        self.rect = Rect(x, y, WIDTH, HEIGHT)
       # self.rect = self.image.get_rect()

        self.animation_timer = pygame.time.get_ticks()
        self.animation_delay = 10
        self.current_frame = 0
        self.MovingLeft = False
        self.MovingRight = False
        self.Jump = False


    def update(self, left, right, up, running, platforms):

        if up:
            if self.onGround:
                self.Jump = True
                self.yvel = -JUMP_POWER
                if running and (left or right):
                    self.yvel -= JUMP_EXTRA_POWER

        if left:
            self.MovingLeft = True
            self.MovingRight = False
            self.xvel = -MOVE_SPEED
            self.image = walkLeft[2]
            if running:
                self.xvel -= MOVE_EXTRA_SPEED

        if right:
            self.MovingRight = True
            self.MovingLeft = False
            self.xvel = MOVE_SPEED
            if running:
                self.xvel += MOVE_EXTRA_SPEED

        if not (left or right):
            self.MovingLeft = False
            self.MovingRight = False
            self.xvel = 0

        if not self.onGround:
            self.Jump = True
            self.yvel += GRAVITY
        if self.onGround:
            self.Jump = False
        self.onGround = False;
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.Animation()

    def Animation(self):
        if pygame.time.get_ticks() - self.animation_timer > self.animation_delay:
            if self.Jump and self.MovingRight:
                self.image = charimageRight
                return
            if self.Jump and self.MovingLeft:
                self.image = charimageLeft
                return
            if self.MovingLeft:
                self.current_frame = (self.current_frame + 1) % len(walkLeft)  # Переход к следующему кадру
                self.image = walkLeft[self.current_frame]
            if self.MovingRight:
                self.current_frame = (self.current_frame + 1) % len(walkRight)  # Переход к следующему кадру
                self.image = walkRight[self.current_frame]
        self.animation_timer = pygame.time.get_ticks()

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):
                if isinstance(p, BlockDie): #or isinstance(p, Monster):
                    self.die()
                elif isinstance(p, BlockTeleport):
                    self.teleporting(p.goX, p.goY)
                elif isinstance(p, Door):
                    self.winner = True
                else:
                    if xvel > 0:
                        self.rect.right = p.rect.left

                    if xvel < 0:
                        self.rect.left = p.rect.right

                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0

                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

#    def drawWindow():
#        global animCount
#
#        if animCount + 1 >= 60:
#            animCount = 0
#
#        if left:
#            screen.blit(walkLeft[animCount // 7], (xvel, yvel))
#            animCount += 1
#        elif right:
#            win.blit(walkLeft[animCount // 7], (xvel, yvel))
#            animCount += 1

    def teleporting(self, goX, goY):
        self.rect.x = goX
        self.rect.y = goY

    def SetPos(self, goX, goY):
        if self.rect.x > goX:
            self.MovingLeft = True
            self.MovingRight = False
        if self.rect.x < goX:
            self.MovingRight = True
            self.MovingLeft = False
        if self.rect.y != goY and self.MovingRight == True:
            self.Jump = True
        if self.rect.y != goY and self.MovingLeft == True:
            self.Jump = True
        if self.rect.y == goY:
            self.Jump == False
        self.Animation()
        self.rect.x = goX
        self.rect.y = goY


    def die(self):
        time.wait(1000)
        self.teleporting(self.startX, self.startY)

    def interpolate_coordinates(self,PrevX, PrevY ,NextX, NextY, previous_timestamp, next_timestamp):
        x = [float(PrevX), float(NextX)]
        y = [float(PrevY), float(NextY)]
        t = [float(previous_timestamp), float(next_timestamp)]
        prevTime = float(previous_timestamp)
        x_interp = scipy.interpolate.interp1d(t, x)
        y_interp = scipy.interpolate.interp1d(t, y)
        while (prevTime <= float(next_timestamp)):
            self.SetPos(float(x_interp(prevTime)), float(y_interp(prevTime)))
            prevTime += (float(next_timestamp)-float(previous_timestamp))/60
        self.SetPos(float(NextX),float(NextY))

