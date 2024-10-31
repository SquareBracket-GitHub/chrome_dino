from utils.sprites import blitSprite
from settings import SCREEN_WIDTH

class GameOver_UI:
    def __init__(self):
        self.visible = False

    def setVisible(self, visible):
        self.visible = visible
    
    def display(self, screen):
        if not self.visible: return
        blitSprite(screen, 'game_over', ((SCREEN_WIDTH - 191)/2, 340))
        blitSprite(screen, 'restart', ((SCREEN_WIDTH - 35)/2, 380))