from pickle import load
from snake import playWithNet
from random import randint
loadin = open("Training143/bestSnakeMAX.pickle", 'rb')
snakenet = load(loadin)

while 1:
    playWithNet(snakenet, randint(2,20000),headless=False, slow=True)