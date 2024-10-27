import pygame
import math

from utils.ground import Ground
from utils.player import Player
from utils.score import ScoreText
from utils.gameover_UI import GameOver_UI
from utils.high_score import writeHighScore, resetHighScore
from utils.ptera import generateRandomPtera
from utils.cactus import generateRandomCactus
from utils.sound import playSound

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PTERA_INTERVAL, CACTUS_INTERVAL, CHECK_POINT, PTERA_SPEED, GROUND_SPEED, CACTUS_INTERVAL_SCALING_SPPED, PTERA_STARTING_SPAWN_SCORE

pygame.init()

pygame.display.set_caption('Chrome Dino')

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

game_speed = 0

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
                    break
                case pygame.K_0:
                    resetHighScore()
                    break
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_status == 'gameover':
                game_status = 'waitng'
                game_speed = 0
                setGame()
    screen.fill(gray)

    if game_speed < PTERA_STARTING_SPAWN_SCORE and game_status == 'playing':
        game_speed += 1

    player.play(screen)
    ground_1.play(screen, game_speed)
    ground_2.play(screen, game_speed)
    scoreText.play(screen)

    gameover.display(screen)

    dontSpawn_ptera = False
    dontSpawn_cactus = False

    for ptera in pteras:
        ptera.play(screen, game_speed)
        ptera_x = ptera.x
        if ptera_x > 0:
            dontSpawn_ptera = True
        if ptera_x < SCREEN_WIDTH - PTERA_INTERVAL:
            del pteras[0]
        if player.mask.overlap(ptera.mask, (ptera.x - player.x, ptera.y - player.y)):
            if game_status != 'gameover':
                playSound(1)
            game_status = 'gameover'
            gameOver()
        
    BLUE = (0, 0, 255)

    if not dontSpawn_ptera and scoreText.score >= PTERA_STARTING_SPAWN_SCORE:
        new_ptera = generateRandomPtera(game_status == 'playing')
        if new_ptera:
            p_d_distance = (new_ptera.x - player.x)
            w = p_d_distance  / (PTERA_SPEED * GROUND_SPEED + game_speed * 0.003)
            moved_cactusArr = []
            for c in cactusArr:
                moved_cactusArr.append(c.x - w * (GROUND_SPEED + game_speed * 0.003))
            for x in moved_cactusArr:
                distance = math.sqrt(math.pow(player.x - x, 2))
                print(distance)
                if distance < 150:
                    dontSpawn_ptera = True
            if not dontSpawn_ptera:
                pteras.append(new_ptera)
    
    deleteList = []

    i = 0
    for cactus in cactusArr:
        cactus.play(screen, game_speed)
        if cactus.x > SCREEN_WIDTH - CACTUS_INTERVAL - (game_speed * CACTUS_INTERVAL_SCALING_SPPED):
            dontSpawn_cactus = True
        if cactus.x < -100:
            deleteList.append(i)

        if player.mask.overlap(cactus.mask, (cactus.x - player.x, cactus.y - player.y)):
            if game_status != 'gameover':
                playSound(1)
            game_status = 'gameover'
            gameOver()   
        i += 1
    
    for e in deleteList:
        del cactusArr[e]
    
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