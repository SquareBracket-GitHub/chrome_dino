from utils.sprites import blitSprite, getHeight, getWidth, getRect, getMask
from utils.sound import playSound
from settings import JUMP_POWER
import pygame
import math

class Player:
    def __init__(self):
        self.x = 60
        self.y = 470
        self.w = 1
        self.h = 1
        self.rect = getRect('dino_idle', (self.x, self.y))
        self.farToGround = 0
        self.jumping = 0
        self.state = 'idle'
        self.substate = ''
        self.frames = 0
        self.animationNum = 0
        self.mask = getMask('dino_idle')

    def stop(self):
        self.state = 'dead'
    
    def jump(self):
        if self.state == 'jumping' or self.state == 'dead' or self.substate != '': return
        self.jumping = JUMP_POWER
        self.state = 'jumping'
        playSound(0)

    def play(self, screen):
        if self.state == 'dead':
            self.y = -self.farToGround + 470
            blitSprite('dino_dead', screen, self.x, self.y)
            return
        
        if pygame.key.get_pressed()[pygame.K_DOWN] and (self.state == 'run' or self.state == 'jumping'):
            self.substate = '_crawl'
        else: self.substate = ''

        if self.substate == '_crawl':
            self.y = -self.farToGround + 487
        else:
            self.y = -self.farToGround + 470
        self.animationNum = math.floor(self.frames / 5)

        if self.state == 'jumping':
            self.farToGround += self.jumping
        else:
            self.farToGround = 0
            self.frames += 1

        if self.animationNum > 1:
            self.frames = 0
            self.animationNum = 0
        
        if self.y > 470:
            self.state = 'run'
        
        if self.substate == '':
            self.jumping -= 0.4
        else:
            self.jumping -= 1

        if self.state == 'idle' or self.state == 'jumping':
            self.w = getWidth('dino_idle' + self.substate)
            self.h = getHeight('dino_idle' + self.substate)
            self.rect = getRect('dino_idle' + self.substate, (self.x, self.y))
            self.mask = getMask('dino_idle' + self.substate)
            blitSprite('dino_idle' + self.substate, screen, self.x, self.y)
        else:
            self.w = getWidth('dino_run0' + str(self.animationNum) + self.substate)
            self.h = getHeight('dino_run0' + str(self.animationNum) + self.substate)
            self.rect = getRect('dino_idle' + self.substate, (self.x, self.y))
            self.mask = getMask('dino_idle' + self.substate)
            blitSprite('dino_run0' + str(self.animationNum) + self.substate, screen, self.x, self.y)