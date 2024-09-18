from utils.sprites import blitSprite
from settings import SCREEN_WIDTH, GROUND_SPEED

class Ground:
    def __init__(self, x):
        self.x = x
        self.y = 500
        self.speed = GROUND_SPEED
        self.moving = False

    def move(self):
        self.moving = True

    def stop(self):
        self.moving = False
        
    def play(self, screen):
        if self.moving:
            self.x -= self.speed
        if self.x <= -SCREEN_WIDTH - 100:
            self.x += 2 * 1200
        
        blitSprite('ground', screen, self.x, self.y)