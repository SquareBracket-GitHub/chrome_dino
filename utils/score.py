from utils.sprites import blitText
from utils.high_score import loadHighScore
from settings import SCREEN_WIDTH

class Score:
    def __init__(self):
        self.score = 0
        self.start = False

    def startScoring(self):
        self.start = True
    
    def stop(self):
        self.start = False

    def scoring(self, screen):
        if self.start:
            self.score += 1