#SCREEN SIZE
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 700

#GROUND_SETTING
GROUND_SPEED = 7                    #땅 이동속도 및 선인장 이동속도

#PLAYER SETTING
JUMP_POWER = 8                      #플레이어 점프 높이

#OBSTACLE SETTING
PTERA_SPEED = 1.3 * GROUND_SPEED    #프테라 속도
PTERA_INTERVAL = SCREEN_WIDTH       #SCREEN_WIDTH에 뺌
CACTUS_INTERVAL = 500               #SCREEN_WIDTH에 뺌
CACTUS_INTERVAL_SCALING_SPEED = 0.0 #선인장 간격 증가 속도
PTERA_STARTING_SPAWN_SCORE = 2000   #프테라가 등장하기 시작하는 점수
PTERA_PROBABILITY = 200             #프레임당 값분의 1
CACTUS_PROBABILITY = 100            #프레임당 값분의 1
UNFAIR_PTERA_CENSOR_RANGE = 150     #불공정한 프테라 센서의 범위 (좌우로)

#SCORE SYSTEM
CHECK_POINT = 300                   #값의 배수마다 체크포인트 효과음

#SOUND SETTING
SOUND_ALLOWED = True