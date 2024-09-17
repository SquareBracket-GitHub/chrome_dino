import pygame
import random

from utils.ground import Ground
from utils.player import Player
from utils.score import ScoreText

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gray = pygame.Color("#F7F7F7")

ground_1 = Ground(0)
ground_2 = Ground(1200)

player = Player()

scoreText = ScoreText()

game_status = 'wating'

pteras = []

def generatePtera():
    random_Y = random.randrange(404, 468)
    pteras.append({'x': SCREEN_WIDTH, 'y': random_Y, 'frame': 0})

generatePtera()

running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    player.jump()
                    break
    screen.fill(gray)

    player.play(screen)
    ground_1.play(screen)
    ground_2.play(screen)
    scoreText.scoring()

    if player.farToGround < 0:
        game_status = 'playing'
        ground_1.moving = True
        ground_2.moving = True
        scoreText.start = True

    scoreText.display(screen, SCREEN_WIDTH)

    # for ptera in pteras:
    #     ptera['frame'] += 1
    #     if math.floor(ptera['frame']/5) > 1: ptera['frame'] = 0
    #     ptera['x'] -= gorund_speed
    #     screen.blit(sprites['ptera0' + str(math.floor(ptera['frame']/5))], (ptera['x'], ptera['y']))
    pygame.display.flip()

    clock.tick(60)