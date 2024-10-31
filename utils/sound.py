import pygame
from settings import SOUND_ALLOWED
import os

pygame.mixer.init()

sounds = [
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/jump.wav')),
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/gameover.wav')),
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/checkPoint.wav'))
]


def playSound(sound):
    '''
    : param sound: 0 - jump sound, 1 - gameover sound, 2 - check point
    '''
    if not SOUND_ALLOWED: return
    sounds[sound].play()