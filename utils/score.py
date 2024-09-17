from utils.sprites import blitText

class ScoreText:
    def __init__(self):
        self.score = 00000
        self.start = False
    def scoring(self):
        if self.start:
            self.score += 1
    def display(self, screen, screen_w):
        blitText(str(self.score), screen, screen_w - 30, 300, 'LEFT')