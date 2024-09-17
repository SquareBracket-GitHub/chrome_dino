import pygame
import xml.etree.ElementTree as ET
import os

xml_path = os.path.abspath('assets/sprites.xml')
spritesheet_path = os.path.abspath('assets/sprites.png')

tree = ET.parse(xml_path)
root = tree.getroot()

spritesheet = pygame.image.load(spritesheet_path)

sprites = {}

for sprite in root.findall('sprite'):
    name = sprite.get('name')
    x = int(sprite.get('x'))
    y = int(sprite.get('y'))
    width = int(sprite.get('width'))
    height = int(sprite.get('height'))

    image = spritesheet.subsurface(pygame.Rect(x, y, width, height))
    sprites[name] = image

def blitSprite(sprite, screen, x=0, y=0):
    return screen.blit(sprites[sprite], (x, y))

def blitText(text, screen, x=0, y=0, direction="RIGHT"):
    space = 0
    spacing = 11
    text_list = list(text)
    if direction == 'LEFT':
        spacing = spacing * -1
        text_list.reverse()
    for i, word in enumerate(text_list):
        blitSprite(word, screen, x + space, y)
        space += spacing