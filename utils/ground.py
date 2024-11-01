from settings import SCREEN_WIDTH, GROUND_SPEED
from utils.sprites import blitSprite
from utils.tuple import editTuple

class Ground:
    def __init__(self, x):
        self.pos = (x, 500)
        self.moving = False

    def move(self):
        self.moving = True

    def stop(self):
        self.moving = False
        
    def play(self, screen, game_speed):
        if self.pos[0] <= -SCREEN_WIDTH - 100:
            self.pos = editTuple(self.pos, 0, self.pos[0] + (2 * 1200))
        if self.moving:
            self.pos = editTuple(self.pos, 0, self.pos[0] - (GROUND_SPEED + (game_speed * 0.003)))
        
        blitSprite(screen, 'ground', self.pos)