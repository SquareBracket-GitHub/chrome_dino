from utils.sprites import blitText
from utils.high_score import loadHighScore
from settings import SCREEN_WIDTH

class ScoreText:
    def play(self, screen, pos=(0,0), direction='RIGHT'):
        blitText(self.content, screen, SCREEN_WIDTH - 30, 300, 'LEFT')