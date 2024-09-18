from utils.sprites import blitSprite
from settings import JUMP_POWER
import pygame
import math
import os

pygame.mixer.init()
jump_sound = pygame.mixer.Sound(os.path.abspath('assets/sounds/jump.mp3'))

class Player:
    def __init__(self):
        self.x = 60
        self.farToGround = 0
        self.y = 470
        self.jumping = 0
        self.state = 'idle'
        self.substate = ''
        self.frames = 0
        self.animationNum = 0

    def stop(self):
        self.state = 'dead'
    
    def jump(self):
        if self.state == 'jumping' or self.state == 'dead': return
        self.jumping = JUMP_POWER
        self.state = 'jumping'
        jump_sound.play()

    def play(self, screen):
        if self.state == 'dead':
            blitSprite('dino_dead', screen, self.x, self.y)
            return
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
        
        if (self.substate == '' and self.farToGround < 0) or (self.substate != '' and self.farToGround < 1):
            self.state = 'run'
        
        if self.substate == '':
            self.jumping -= 0.4
        else:
            self.jumping -= 1
        
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.substate = '_crawl'
        else: self.substate = ''

        if self.state == 'idle' or self.state == 'jumping':
            blitSprite('dino_idle' + self.substate, screen, self.x, self.y)
        else:
            blitSprite('dino_run0' + str(self.animationNum) + self.substate, screen, self.x, self.y)