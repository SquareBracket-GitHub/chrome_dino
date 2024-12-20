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

def blitSprite(screen, sprite, pos=(0,0)):
    return screen.blit(sprites[sprite], pos)

def blitText(screen, content='', pos=(0,0), direction='RIGHT'):
    space = 0
    spacing = 11
    text_list = list(content)
    if direction == 'LEFT':
        spacing = spacing * -1
        text_list.reverse()
    for word in enumerate(text_list):
        if word[1] != ' ':
            blitSprite(screen, word[1], (pos[0] + space, pos[1]))
        space += spacing

def getMask(sprite):
    return pygame.mask.from_surface(sprites[sprite])