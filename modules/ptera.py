import random
import math

from settings import SCREEN_WIDTH, PTERA_SPEED, PTERA_PROBABILITY
from modules.sprites import blitSprite, getMask
from modules.tuple import editTuple

class Ptera:
    def __init__(self):
        self.pos = (SCREEN_WIDTH, random.randrange(394, 458))
        self.frames = 0
        self.animation_num = 0
        self.moving = False
        self.is_game_over = False
        self.mask = getMask('ptera00')
    
    def stop(self):
        self.is_game_over = True
    
    def move(self):
        self.moving = True
    
    def play(self, screen, game_speed):
        #If player died
        if self.is_game_over:
            blitSprite(screen, 'ptera0' + str(self.animation_num), self.pos)
            return
        
        self.pos = editTuple(self.pos, 0, self.pos[0] - (PTERA_SPEED + (game_speed * 0.003)))

        self.frames += 1
        self.animation_num = math.floor(self.frames / 5)

        #animation number reset
        if self.animation_num > 1:
            self.frames = 0
            self.animation_num = 0

        self.mask = getMask('ptera0' + str(self.animation_num))
        blitSprite(screen, 'ptera0' + str(self.animation_num), self.pos)

def generateRandomPtera(isPlaying):
    if not isPlaying:
        return
    random_chance = random.randrange(1, PTERA_PROBABILITY + 1)
    if random_chance <= 1:
        return Ptera()