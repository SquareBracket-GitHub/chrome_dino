import pygame
import random

from utils.ground import Ground
from utils.player import Player
from utils.score import ScoreText
from utils.gameover_UI import GameOver_UI
from utils.high_score import writeHighScore

from settings import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

gray = pygame.Color("#F7F7F7")

ground_1 = Ground(0)
ground_2 = Ground(1200)

player = Player()

scoreText = ScoreText()

gameover = GameOver_UI()

game_status = 'wating'

pteras = []

def generatePtera():
    random_Y = random.randrange(404, 468)
    pteras.append({'x': SCREEN_WIDTH, 'y': random_Y, 'frame': 0})

generatePtera()

def gameOver():
    ground_1.stop()
    ground_2.stop()
    scoreText.stop()
    player.stop()
    gameover.setVisible(True)
    writeHighScore(scoreText.score)

def setGame():
    ground_1.__init__(0)
    ground_2.__init__(1200)
    scoreText.__init__()
    player.__init__()
    gameover.__init__()
    scoreText.__init__()

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
                case pygame.K_DELETE:
                    game_status = 'gameover'
                    gameOver()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_status == 'gameover':
                game_status = 'waitng'
                setGame()
    screen.fill(gray)

    player.play(screen)
    ground_1.play(screen)
    ground_2.play(screen)
    scoreText.play(screen)

    gameover.display(screen)

    if player.farToGround < 0:
        game_status = 'playing'
        ground_1.move()
        ground_2.move()
        scoreText.startScoring()

    # for ptera in pteras:
    #     ptera['frame'] += 1
    #     if math.floor(ptera['frame']/5) > 1: ptera['frame'] = 0
    #     ptera['x'] -= gorund_speed
    #     screen.blit(sprites['ptera0' + str(math.floor(ptera['frame']/5))], (ptera['x'], ptera['y']))
    pygame.display.flip()

    clock.tick(60)