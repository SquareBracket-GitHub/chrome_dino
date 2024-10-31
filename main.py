import pygame
import math

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PTERA_INTERVAL, CACTUS_INTERVAL, CHECK_POINT, PTERA_SPEED, GROUND_SPEED, CACTUS_INTERVAL_SCALING_SPEED, PTERA_STARTING_SPAWN_SCORE, UNFAIR_PTERA_CENSOR_RANGE
from utils.ground import Ground
from utils.player import Player
from utils.gameover_UI import GameOver_UI
from utils.high_score import writeHighScore, resetHighScore, loadHighScore
from utils.sound import playSound
from utils.sprites import blitText
from utils.ptera import generateRandomPtera
from utils.cactus import generateRandomCactus

#pygame init
pygame.init()

#set pygame
pygame.display.set_caption('Chrome Dino')

icon_img = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon_img)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#define color
GRAY = pygame.Color("#F7F7F7")
BLUE = pygame.Color("#0000FF")

#init sprites
ground_1 = Ground(0)
ground_2 = Ground(1200)
player = Player()
gameover_UI = GameOver_UI()
ptera_arr = []
cactus_arr = []

#game variables
game_status = 'wating'
game_score = 0
game_speed = 0

#game functions
def gameOver():
    global game_status

    if game_status != 'gameover':
        playSound(1)

    game_status = 'gameover'

    player.stop()
    ground_1.stop()
    ground_2.stop()
    gameover_UI.setVisible(True)

    for ptera in ptera_arr:
        ptera.stop()
    for cactus in cactus_arr:
        cactus.stop()

    writeHighScore(game_score)

def resetGame():
    global game_status
    global game_score
    global game_speed

    game_status = 'wating'
    game_score = 0
    game_speed = 0

    ground_1.__init__(0)
    ground_2.__init__(1200)
    player.__init__()
    gameover_UI.__init__()

    ptera_arr.clear()
    cactus_arr.clear()

def detectCollision(object1, object2):
    return object1.mask.overlap(object2.mask, (object2.pos[0] - object1.pos[0], object2.pos[1] - object1.pos[1]))

running = True
clock = pygame.time.Clock()

#game
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
                    gameOver()
                    break
                case pygame.K_0:
                    resetHighScore()
                    break
        if event.type == pygame.MOUSEBUTTONDOWN:
                if game_status == 'gameover':
                    resetGame()
    
    screen.fill(GRAY)

    if game_status == 'playing':
        #scoring
        game_score += 1

        #increasing game speed
        if game_speed < PTERA_STARTING_SPAWN_SCORE:
            game_speed += 1

    #scoreText content
    high_score = loadHighScore()
    scoreText_content = ''
    if high_score == None or high_score == '':
        scoreText_content = str(game_score)
    else:
        scoreText_content = 'HI ' + high_score + ' ' + str(game_score)
    
    #playing sprites
    player.play(screen)
    ground_1.play(screen, game_speed)
    ground_2.play(screen, game_speed)
    gameover_UI.display(screen)
    blitText(screen, scoreText_content, (SCREEN_WIDTH - 30, 300), 'LEFT')

    dont_spawn_ptera = False
    for ptera in ptera_arr:
        ptera.play(screen, game_speed)
        if ptera.pos[0] > 0:
            dont_spawn_ptera = True
        if ptera.pos[0] < SCREEN_WIDTH - PTERA_INTERVAL:
            del ptera_arr[0]
        
        isCollided = detectCollision(player, ptera)
        if isCollided:
            gameOver()

    dont_spawn_cactus = False
    delete_cactus_arr = []
    i = 0
    for cactus in cactus_arr:
        cactus.play(screen, game_speed)
        if cactus.pos[0] > SCREEN_WIDTH - CACTUS_INTERVAL - (game_speed * CACTUS_INTERVAL_SCALING_SPEED):
            dont_spawn_cactus = True
        if cactus.pos[0] < -100:
            delete_cactus_arr.append(i)
        
        isCollided = detectCollision(player, cactus)
        if isCollided:
            gameOver()

        i += 1
    
    for d in delete_cactus_arr:
        del cactus_arr[d]
    
    #spawn ptera
    if not dont_spawn_ptera and game_score >= PTERA_STARTING_SPAWN_SCORE:
        new_ptera = generateRandomPtera(game_status == 'playing')
        if new_ptera:
            p_d_distance = (new_ptera.pos[0] - player.pos[0])
            t = p_d_distance  / (PTERA_SPEED  + game_speed * 0.003)
            moved_cactus_arr = []
            for c in cactus_arr:
                moved_cactus_arr.append(c.pos[0] - t * (GROUND_SPEED + game_speed * 0.003))
            for x in moved_cactus_arr:
                distance = math.sqrt(math.pow(player.pos[0] - x, 2))
                if distance < UNFAIR_PTERA_CENSOR_RANGE:
                    dont_spawn_ptera = True
            if not dont_spawn_ptera:
                ptera_arr.append(new_ptera)
    
    #spawn cactus
    if not dont_spawn_cactus:
        new_cactus = generateRandomCactus(game_status == 'playing')
        if new_cactus:
            cactus_arr.append(new_cactus)
    
    #sound
    if game_score % CHECK_POINT == 0 and game_score != 0:
        playSound(2)
    
    #starting game event
    if player.far_to_ground < 0:
        game_status = 'playing'
        ground_1.move()
        ground_2.move()
        for ptera in ptera_arr:
            ptera.move()
        for cactus in cactus_arr:
            cactus.move()
    
    pygame.display.flip()

    clock.tick(60)