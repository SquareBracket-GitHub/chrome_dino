import pygame
import math
import datetime

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PTERA_INTERVAL, CACTUS_INTERVAL, CHECK_POINT, PTERA_SPEED, GROUND_SPEED, CACTUS_INTERVAL_SCALING_SPEED, PTERA_STARTING_SPAWN_SCORE, UNFAIR_PTERA_CENSOR_RANGE
from modules.ground import Ground
from modules.player import Player
from modules.gameover_UI import GameOver_UI
from modules.high_score import writeHighScore, resetHighScore, loadHighScore
from modules.sound import playSound
from modules.sprites import blitText
from modules.ptera import generateRandomPtera
from modules.cactus import generateRandomCactus

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
game_status = 'waiting'
game_score = 0
game_speed = 0

#game functions
def gameOver():
    global game_status

    if game_status != 'gameover':
        playSound(1)

        now = datetime.datetime.now()
        print('Event: Gameover (present score: ' + str(game_score) + ', datetime: ' + str(now) + ')')

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

    game_status = 'waiting'
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
                    print('Event: Dying Cheat (present score: ' + str(game_score) + ')')
                    gameOver()
                    break
                case pygame.K_0:
                    print('Event: Reset High Score (high score: ' + loadHighScore() + ')')
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
                print("Event: New Ptera (spawn)")
            else: print("Event: New Ptera (don't spawn)")
    
    #spawn cactus
    if not dont_spawn_cactus:
        new_cactus = generateRandomCactus(game_status == 'playing')
        if new_cactus:
            cactus_arr.append(new_cactus)
    
    #sound
    if game_score % CHECK_POINT == 0 and game_score != 0:
        playSound(2)
    
    #starting game event
    if player.far_to_ground < 0 and game_status == 'waiting':
        game_status = 'playing'
        ground_1.move()
        ground_2.move()

    pygame.display.flip()

    clock.tick(60)