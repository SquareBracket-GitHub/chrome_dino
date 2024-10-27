import os

def loadHighScore():
    path = os.path.abspath('data/HIGH_SCORE.TXT')

    if not os.path.isfile(path):
        f = open(path, "w")
        f.write("")
        f.close()
        return None

    f = open(path, 'r')
    data = f.read()
    f.close()
    return data

def isHighScore(score):
    hs = loadHighScore()
    if hs == '':
        hs = 0
    return score > int(hs)

def writeHighScore(score):
    if not isHighScore(score):
        return
    
    path = os.path.abspath('data/HIGH_SCORE.TXT')
    f = open(path, 'w')
    f.write(str(score))
    f.close

def resetHighScore():
    path = os.path.abspath('data/HIGH_SCORE.TXT')
    if os.path.exists(path):
        os.remove(path)