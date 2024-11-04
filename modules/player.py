import pygame
import math

from settings import JUMP_POWER
from modules.sprites import blitSprite, getMask
from modules.sound import playSound
from modules.tuple import editTuple

class Player:
    def __init__(self):
        self.pos = (60, 470)
        self.far_to_ground = 0
        self.jumping = 0
        self.state = 'idle'
        self.substate = ''
        self.frames = 0
        self.animation_num = 0
        self.mask = getMask('dino_idle')

    def stop(self):
        self.state = 'dead'

    def jump(self):
        if self.state == 'jumping' or self.state == 'dead' or self.substate != '': return
        self.jumping = JUMP_POWER
        self.state = 'jumping'
        playSound(0)

    def play(self, screen):
        #If player died
        if self.state == 'dead':
            blitSprite(screen, 'dino_dead', self.pos)
            return
        
        self.pos = editTuple(self.pos, 1, -self.far_to_ground + 470)
        
        #crawl
        if pygame.key.get_pressed()[pygame.K_DOWN] and (self.state == 'run' or self.state == 'jumping'):
            self.substate = '_crawl'
        else: self.substate = ''

        #jump
        if self.state == 'jumping':
            self.far_to_ground += self.jumping
        else:
            self.far_to_ground = 0
            self.frames += 1
        
        self.animation_num = math.floor(self.frames / 5)
        
        #animation number reset
        if self.animation_num > 1:
            self.frames = 0
            self.animation_num = 0
        
        if self.pos[1] > 470:
            self.state = 'run'
        
        if self.substate == '':
            self.jumping -= 0.4
        else:
            self.jumping -= 1
        
        if self.state == 'idle' or self.state == 'jumping':
            self.mask = getMask('dino_idle' + self.substate)
            blitSprite(screen, 'dino_idle' + self.substate, self.pos)
        else:
            self.mask = getMask('dino_run0' + str(self.animation_num) + self.substate)
            blitSprite(screen, 'dino_run0' + str(self.animation_num) + self.substate, self.pos)