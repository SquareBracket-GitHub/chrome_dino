import pygame
from settings import SOUND_ALLOWED
import os

pygame.mixer.init()

sounds = [
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/jump.wav')),
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/die.wav')),
    pygame.mixer.Sound(os.path.abspath('./assets/sounds/checkPoint.wav'))
]

def playSound(sound):
    if not SOUND_ALLOWED: return
    sounds[sound].play()