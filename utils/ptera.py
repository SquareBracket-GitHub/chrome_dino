import random
from settings import SCREEN_WIDTH, GROUND_SPEED, PTERA_SPEED, PTERA_PROBABILITY
from utils.sprites import blitSprite, getWidth, getHeight, getRect, getMask
import math

class Ptera:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randrange(404, 468)
        self.w = 1
        self.h = 1
        self.rect = getRect('ptera00', (self.x, self.y))
        self.frames = 0
        self.animationNum = 0
        self.moving = False
        self.isGameOver = False
        self.mask = getMask('ptera00')

    def stop(self):
        self.isGameOver = True
    
    def move(self):
        self.moving = True

    def play(self, screen, score):
        if self.isGameOver:
            blitSprite('ptera0' + str(self.animationNum), screen, self.x, self.y)
            return
        self.x -= GROUND_SPEED * PTERA_SPEED + (score * 0.002)
        self.frames += 1
        self.animationNum = math.floor(self.frames/5)
        if self.animationNum > 1:
            self.frames = 0
            self.animationNum = 0
        self.w = getWidth('ptera0' + str(self.animationNum))
        self.h = getHeight('ptera0' + str(self.animationNum))
        self.rect = getRect('ptera0' + str(self.animationNum), (self.x, self.y))
        self.mask = getMask('ptera0' + str(self.animationNum))
        addY = 0
        if self.animationNum == 1:
            addY = -6
        blitSprite('ptera0' + str(self.animationNum), screen, self.x, self.y + addY)

def generateRandomPtera(isPlaying):
    if not isPlaying:
        return
    randomChance = random.randrange(1, PTERA_PROBABILITY + 1)
    if randomChance <= 1:
        return Ptera()