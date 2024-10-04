from settings import SCREEN_WIDTH, CACTUS_PROBABILITY
from utils.sprites import blitSprite, getRect, getMask
from settings import GROUND_SPEED
import random

class Cactus():
    def __init__(self, img):
        self.x = SCREEN_WIDTH
        self.y = 470
        self.w = 1
        self.h = 1
        self.rect = getRect('ptera00', (self.x, self.y))
        self.img = img
        self.moving = False
        self.isGameOver = False
        self.mask = getMask(self.img)

    def stop(self):
        self.isGameOver = True
    
    def move(self):
        self.moving = True

    def play(self, screen, score):
        if self.isGameOver:
            blitSprite(self.img, screen, self.x, self.y)
            return
        self.x -= GROUND_SPEED + (score * 0.002)

        self.rect = getRect(self.img, (self.x, self.y))

        blitSprite(self.img, screen, self.x, self.y)

def generateRandomCactus(isPlaying):
    if not isPlaying:
        return
    randomChance = random.randrange(1, CACTUS_PROBABILITY + 1) # 1 to 100
    if randomChance <= 5:
        size = 'small'
        type = 0
        randomType = random.randrange(1, 7) # 1 to 6
        if randomType > 3:
            size = 'large'
            type = randomType - 4
        return Cactus(size + '_cactus0' + str(type))