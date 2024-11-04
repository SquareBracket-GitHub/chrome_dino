import random

from settings import SCREEN_WIDTH, GROUND_SPEED, CACTUS_PROBABILITY
from modules.sprites import blitSprite, getMask
from modules.tuple import editTuple

class Cactus():
    def __init__(self, sprite):
        self.pos = (SCREEN_WIDTH, 470)
        self.sprite = sprite
        self.moving = True
        self.mask = getMask(self.sprite)
    
    def stop(self):
        self.moving = False
    
    def move(self):
        self.moving = True
    
    def play(self, screen, game_speed):
        if not self.moving:
            blitSprite(screen, self.sprite, self.pos)
            return
        self.pos = editTuple(self.pos, 0, self.pos[0] - (GROUND_SPEED + (game_speed * 0.003)))

        blitSprite(screen, self.sprite, self.pos)

def generateRandomCactus(isPlaying):
    if not isPlaying:
        return
    random_chance = random.randrange(1, CACTUS_PROBABILITY + 1) #1 to 100
    if random_chance <= 5:
        size = 'small'
        type = 0
        random_type = random.randrange(1, 7) #1 to 6
        if random_type > 3:
            size = 'large'
            type = random_type - 4
        return Cactus(size + '_cactus0' + str(type))
