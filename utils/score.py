from utils.sprites import blitText
from utils.high_score import loadHighScore
from settings import SCREEN_WIDTH

class ScoreText:
    def __init__(self):
        self.score = 00000
        self.start = False
        self.content = ''

    def startScoring(self):
        self.start = True
    
    def stop(self):
        self.start = False

    def play(self, screen):
        hs = loadHighScore()
        if hs == None or hs == '':
            self.content = str(self.score)
        else:
            self.content = 'HI ' + hs + ' ' + str(self.score)

        blitText(self.content, screen, SCREEN_WIDTH - 30, 300, 'LEFT')
        if self.start:
            self.score += 1