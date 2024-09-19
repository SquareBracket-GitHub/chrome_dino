from settings import SCREEN_WIDTH
from utils.sprites import blitSprite, getRect
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

    def stop(self):
        self.isGameOver = True
    
    def move(self):
        self.moving = True

    def play(self, screen):
        if self.isGameOver:
            blitSprite(self.img, screen, self.x, self.y)
            return
        self.x -= GROUND_SPEED

        self.rect = getRect(self.img, (self.x, self.y))

        blitSprite(self.img, screen, self.x, self.y)

def generateRandomCactus(isPlaying):
    if not isPlaying:
        return
    randomChance = random.randrange(1, 101) # 1 to 100
    if randomChance <= 5:
        size = 'small'
        type = 0
        randomType = random.randrange(1, 7) # 1 to 6
        if randomType > 3:
            size = 'large'
            type = randomType - 4
        return Cactus(size + '_cactus0' + str(type))