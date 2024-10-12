import pygame
import random
import math

from utils.ground import Ground
from utils.player import Player
from utils.score import ScoreText
from utils.gameover_UI import GameOver_UI
from utils.high_score import writeHighScore
from utils.ptera import generateRandomPtera
from utils.cactus import generateRandomCactus
from utils.sound import playSound

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PTERA_INTERVAL, CACTUS_INTERVAL, CHECK_POINT, PTERA_SPEED, GROUND_SPEED

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
cactusArr = []

def gameOver():
    ground_1.stop()
    ground_2.stop()
    scoreText.stop()
    player.stop()
    for ptera in pteras:
        ptera.stop()
    for cactus in cactusArr:
        cactus.stop()
    gameover.setVisible(True)
    writeHighScore(scoreText.score)

def setGame():
    ground_1.__init__(0)
    ground_2.__init__(1200)
    scoreText.__init__()
    player.__init__()
    gameover.__init__()
    scoreText.__init__()
    pteras.clear()
    cactusArr.clear()

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
                    if game_status != 'gameover':
                        playSound(1)
                    game_status = 'gameover'
                    gameOver()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_status == 'gameover':
                game_status = 'waitng'
                setGame()
    screen.fill(gray)

    player.play(screen)
    ground_1.play(screen, scoreText.score)
    ground_2.play(screen, scoreText.score)
    scoreText.play(screen)

    gameover.display(screen)

    dontSpawn_ptera = False
    dontSpawn_cactus = False

    for ptera in pteras:
        ptera.play(screen, scoreText.score)
        ptera_x = ptera.x
        if ptera_x > 0:
            dontSpawn_ptera = True
        if ptera_x < SCREEN_WIDTH - PTERA_INTERVAL:
            del pteras[0]
        # if player.rect.colliderect(ptera.rect):
        #     if game_status != 'gameover':
        #         playSound(1)
        #     game_status = 'gameover'
        #     gameOver()
        if player.mask.overlap(ptera.mask, (ptera.x - player.x, ptera.y - player.y)):
            if game_status != 'gameover':
                playSound(1)
            game_status = 'gameover'
            gameOver()
        
    BLUE = (0, 0, 255)
    # pygame.draw.circle(screen, BLUE, [player.x + 65, 440], 40)

    if not dontSpawn_ptera:
        new_ptera = generateRandomPtera(game_status == 'playing')
        if new_ptera:
            print('------------ new ptera was generated ------------')
            i = 0
            print('cactus_speed: ' + str(GROUND_SPEED) + ', ptera_speed: ' + str(PTERA_SPEED))
            print('game_speed: ' + str(scoreText.score * 0.002))
            print('ptera: (' + str(new_ptera.x) + ', ' + str(new_ptera.y) + ')')
            print('dino: (' + str(player.x) + ', 470)')
            for c in cactusArr:
                censor_pos = (player.x + 85, 420)
                censor_r = 40
                w = math.sqrt(math.pow(player.x + 65 - new_ptera.x, 2)) / (GROUND_SPEED + scoreText.score * 0.002)
                p_x = new_ptera.x - (w * (GROUND_SPEED * PTERA_SPEED + scoreText.score * 0.002))
                distance = math.sqrt(math.pow(p_x - censor_pos[0], 2) + math.pow(new_ptera.y - censor_pos[1], 2))
                print(distance, censor_r)
                if distance <= censor_r:
                    dontSpawn_ptera = True
                    print("return: Do not spawn")
            if not dontSpawn_ptera:
                pteras.append(new_ptera)
    
    deleteList = []

    i = 0
    for cactus in cactusArr:
        cactus.play(screen, scoreText.score)
        pygame.draw.circle(screen, (0, 0, 255), [SCREEN_WIDTH - CACTUS_INTERVAL - (scoreText.score * 0.1), 470], 20)
        if cactus.x > SCREEN_WIDTH - CACTUS_INTERVAL - (scoreText.score * 1):
            dontSpawn_cactus = True
        if cactus.x < -100:
            deleteList.append(i)

        # if player.rect.colliderect(cactus.rect):
        #     if game_status != 'gameover':
        #         playSound(1)
        #     game_status = 'gameover'
        #     gameOver()
        if player.mask.overlap(cactus.mask, (cactus.x - player.x, cactus.y - player.y)):
            if game_status != 'gameover':
                playSound(1)
            game_status = 'gameover'
            gameOver()   
        i += 1
    
    for e in deleteList:
        del cactusArr[e]
        print('deleted')
    
    if not dontSpawn_cactus:
        new_cactus = generateRandomCactus(game_status == 'playing')
        if new_cactus:
            cactusArr.append(new_cactus)

    if player.farToGround < 0:
        game_status = 'playing'
        ground_1.move()
        ground_2.move()
        for ptera in pteras:
            ptera.move()
        for cactus in cactusArr:
            cactus.move()
        scoreText.startScoring()

    if scoreText.score % CHECK_POINT == 0 and scoreText.score != 0:
        playSound(2)

    pygame.display.flip()

    clock.tick(60)