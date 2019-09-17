import pygame, sys
from pygame.locals import QUIT, K_RIGHT, K_LEFT, K_UP, K_DOWN
from enum import Enum
from random import randint, seed
from time import sleep
from pickle import dump, load
from neat import *



width = 500
height = 500


squareSize = 20
moveSpeed = 20



def lose(screen,snake):

    screen.fill((255,0,0))
    pygame.display.flip()
    snake.reset()
    sleep(3)




#pygame.key.set_repeat(400, 30)



def getRandSquare():

    mX = width // squareSize
    mY = height // squareSize

    x = randint(0, mX-1) * squareSize
    y = randint(0, mY-1) * squareSize

    return [x,y]

foodLoc = getRandSquare()


class direction(Enum):
    Right = 1
    Left = 2
    Up = 3
    Down = 4


class Snake:

    def __init__(self):

        self.x = randint(1,8) * 50
        self.y = randint(1,8) * 50
        self.direction = direction.Left

        self.tail = []
        self.tail.append([self.x//squareSize * squareSize, self.y//squareSize * squareSize])
        self.size = 3
        self.life = 100

    def reset(self):
        self.x = 50
        self.y = 50
        self.direction = direction.Left

        self.tail = []
        self.tail.append([self.x // squareSize * squareSize, self.y // squareSize * squareSize])
        self.size = 10
        self.life = 200




    def move(self):
        global foodLoc

        if(self.direction == direction.Right):
            self.x += moveSpeed

        if(self.direction == direction.Left):
            self.x -= moveSpeed

        if(self.direction == direction.Up):
            self.y -= moveSpeed

        if(self.direction == direction.Down):
            self.y += moveSpeed

        if(  [self.x//squareSize * squareSize, self.y//squareSize * squareSize] not in self.tail):
            self.tail.append([self.x // squareSize * squareSize, self.y // squareSize * squareSize])



        if(len(self.tail) > self.size):
            del(self.tail[0])

        if(self.tail[-1] == foodLoc):

            foodLoc = getRandSquare()
            self.size+=1
            self.life = 200



def playWithNet(network, rseed, headless=False, slow=False):
    global foodLoc
    seed(rseed)
    if not headless:
        pygame.init()
        screen = pygame.display.set_mode((width, height))
        if slow:
            clock = pygame.time.Clock()

    foodLoc = getRandSquare()
    snake = Snake()

    if len(network.layers[-1].neurons) != 4:
        raise Exception("There are not 4 output neurons!")

    inputs = []
    for n in network.layers[0].neurons:
        inputs.append(n.connections[0].parent)

    inputDict = {"foodU": inputs[0], "foodR": inputs[1], "wallU": inputs[2], "wallR": inputs[3],
                 "wallD": inputs[4], "wallL": inputs[5], "foodD": inputs[6], "foodL": inputs[7]}


                 #"bodU":inputs[8], "bodR":inputs[9], "bodD":inputs[10], "bodL":inputs[11]}


    numFrames = 0
    badMoves = 0
    turns = 0
    while True:
        numFrames += 1
        snake.life-=1
        if(snake.life <0):
            print("dead")
            break

        if not headless:
            if slow:
                clock.tick(30)
            pygame.event.get()

            for event in pygame.event.get():  # wait for events
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()



        # Get output from neural network
        nValues = []

        for n in network.layers[-1].neurons:
            nValues.append(n.value)

        maxVal = max(nValues)
        index = nValues.index(maxVal)

        tempDir = deepcopy(snake.direction)

        if index == 0:
            if snake.direction == direction.Down:
                break
            snake.direction = direction.Up

        elif index == 1:
            if snake.direction == direction.Left:
                break
            snake.direction = direction.Right

        elif index == 2:
            if snake.direction == direction.Up:
                break

            snake.direction = direction.Down

        elif index == 3:
            if snake.direction == direction.Right:
                break
            snake.direction = direction.Left

        else:
            # print("bad move")
            badMoves += 1



        snake.move()
        # Give nerual net input and calculate new values

        # bodUDist = height
        # for j in range(1, snake.y // squareSize):
        #     if [snake.x // squareSize, (snake.y // squareSize) - (squareSize * j)] in snake.tail:
        #         bodUDist = (j * squareSize) - squareSize
        #
        #         break
        #
        # bodRDist = width
        # for j in range(1, width - (snake.x // squareSize)):
        #     if [(snake.x // squareSize) - (squareSize * j), snake.y // squareSize] in snake.tail:
        #         bodRDist = (j * squareSize) - squareSize
        #
        #         break
        #
        # bodDDist = height
        # for j in range(1, height - (snake.y // squareSize)):
        #     if [snake.x // squareSize, (snake.y // squareSize) + (squareSize * j)] in snake.tail:
        #         bodDDist = (j * squareSize) - squareSize
        #         print("$$$" + str(bodDDist))
        #         break
        #
        # bodLDist = width
        # for j in range(1, snake.x // squareSize):
        #     if [(snake.x // squareSize) - (squareSize * j), snake.y // squareSize] in snake.tail:
        #         bodLDist = (j * squareSize) - squareSize
        #         print("$$$" + str(bodLDist))
        #         break

        foodU = (snake.y - foodLoc[1]) / height
        if foodU <0:
            foodU = 1


        foodR =(foodLoc[0] - snake.x) / width
        if foodR < 0:
            foodR = 1

        foodD = (foodLoc[1] - snake.y) / height
        if foodD < 0:
            foodD = 1

        foodL = (snake.x - foodLoc[0]) / width
        if foodL < 0:
            foodL = 1

        inputDict["foodU"].value = foodU
        inputDict["foodR"].value = foodR
        inputDict["wallU"].value = snake.y / height
        inputDict["wallR"].value = (width - snake.x) / width
        inputDict["wallD"].value = (height - snake.y) / height
        inputDict["wallL"].value = snake.x / height
        inputDict["foodD"].value = foodD
        inputDict["foodL"].value = foodL
        # inputDict["bodD"].value = bodDDist/height
        # inputDict["bodL"].value = bodLDist/width
        # inputDict["bodR"].value = bodRDist/width
        # inputDict["bodU"].value = bodUDist/height

        # inputDict["foodDist"].value = math.sqrt( (snake.x - foodLoc[0])**2 + (snake.y - foodLoc[1])**2) / 500

        # print("*******")
        #
        # for x in inputDict.keys():
        #     print( x + ' ' + str(inputDict[x].value))

        network.runNetwork()


        if not headless:
            screen.fill((0, 0, 0))

            for x in range(0, width, squareSize):
                pygame.draw.line(screen, (255, 255, 255), [x, 0], [x, height], 1)
                pygame.draw.line(screen, (255, 255, 255), [0, x], [width, x], 1)

            for t in snake.tail:
                pygame.draw.rect(screen, (0, 255, 255), [t[0], t[1], squareSize, squareSize])

            pygame.draw.rect(screen, (255, 0, 0), [foodLoc[0], foodLoc[1], squareSize, squareSize])

            pygame.display.flip()



        # Check loss
        collision = [snake.x // squareSize * squareSize, snake.y // squareSize * squareSize] in snake.tail[
                                                                                                0:len(snake.tail) - 1]
        out = snake.y > height-squareSize or snake.y < 0 or snake.x > width-squareSize or snake.x < 0
        if collision or out:
            break



    return snake.size* 20 + numFrames


def playWithHuman():
    global foodLoc

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    foodLoc = getRandSquare()
    snake = Snake()
    sleep(2)




    numFrames = 0
    badMoves = 0
    turns = 0
    while True:
        numFrames += 1


        clock.tick(15)
        pygame.event.get()

        for event in pygame.event.get():  # wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        snake.move()

        # Get output from neural network

        keys = pygame.key.get_pressed()


        tempDir = deepcopy(snake.direction)

        if keys[K_LEFT] and snake.direction != direction.Right:
            snake.direction = direction.Left
        elif keys[K_RIGHT] and snake.direction != direction.Left:
            snake.direction = direction.Right
        elif keys[K_UP] and snake.direction != direction.Down:
            snake.direction = direction.Up
        elif keys[K_DOWN] and snake.direction != direction.Up:
            snake.direction = direction.Down

        else:
            # print("bad move")
            badMoves += 1

        if tempDir != snake.direction:
            turns += 1

        # Give nerual net input and calculate new values



        # inputDict["foodDist"].value = math.sqrt( (snake.x - foodLoc[0])**2 + (snake.y - foodLoc[1])**2) / 500



        screen.fill((0, 0, 0))

        for x in range(0, width, squareSize):
            pygame.draw.line(screen, (255, 255, 255), [x, 0], [x, height], 1)
            pygame.draw.line(screen, (255, 255, 255), [0, x], [width, x], 1)

        for t in snake.tail:
            pygame.draw.rect(screen, (0, 255, 255), [t[0], t[1], squareSize, squareSize])

        pygame.draw.rect(screen, (255, 0, 0), [foodLoc[0], foodLoc[1], squareSize, squareSize])

        pygame.display.flip()

        # Check loss
        collision = [snake.x // squareSize * squareSize, snake.y // squareSize * squareSize] in snake.tail[
                                                                                                0:len(snake.tail) - 1]
        out = snake.y > height-squareSize or snake.y < 0 or snake.x > width-squareSize or snake.x < 0
        if collision or out:
            break

        if (snake.size / numFrames < .001):
            print("loop")
            break

    return snake.size * 20 + numFrames + turns
