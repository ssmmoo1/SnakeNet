from neat import *
from snake import *

maxFrames = 0
for x in range(10000):
    net = genRandNet(5, 4, [3, 4], [2, 4], [-5, 5])
    score = playWithNet(net)
    #print(score[1])
    if score[1] > maxFrames:
        maxFrames = score[1]

print(maxFrames)