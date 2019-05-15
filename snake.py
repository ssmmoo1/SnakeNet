import pygame, sys
from pygame.locals import QUIT, K_RIGHT, K_LEFT, K_UP, K_DOWN
from enum import Enum
from random import randint
from time import sleep

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

        self.x = 50
        self.y = 50
        self.direction = direction.Right

        self.tail = []
        self.tail.append([self.x//squareSize * squareSize, self.y//squareSize * squareSize])
        self.size = 3

    def reset(self):
        self.x = 50
        self.y = 50
        self.direction = direction.Right

        self.tail = []
        self.tail.append([self.x // squareSize * squareSize, self.y // squareSize * squareSize])
        self.size = 10




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







def playWithNetHeadLess(network):


    snake = Snake()
    if len(network.layers[0].neurons) != 5:
        raise Exception("There are not 5 input neurons!")

    if len(network.layers[-1].neurons) != 4:
        raise Exception("There are not 4 output neurons!")

    inputs = []
    for n in network.layers[0].neurons:
        inputs.append(n.connections[0].parent)

    inputDict = {"size": inputs[0], "snakeX": inputs[1], "snakeY": inputs[2], "foodX": inputs[3], "foodY": inputs[4]}
    numFrames = 0
    while True:
        numFrames+=1
        snake.move()

        # Get output from neural network
        nValues = []

        for n in network.layers[-1].neurons:
            nValues.append(n.value)

        maxVal = max(nValues)
        index = nValues.index(maxVal)

        if index == 0:
            snake.direction = direction.Up

        elif index == 1:
            snake.direction = direction.Right

        elif index == 2:
            snake.direction = direction.Down

        elif index == 3:
            snake.direction = direction.Left

        # Give nerual net input and calculate new values

        inputDict["size"].value = snake.size
        inputDict["snakeX"].value = snake.x
        inputDict["snakeY"].value = snake.y
        inputDict["foodX"].value = foodLoc[0]
        inputDict["foodY"].value = foodLoc[1]

        network.runNetwork()


        #Check loss
        collision = [snake.x // squareSize * squareSize, snake.y // squareSize * squareSize] in snake.tail[
                                                                                                0:len(snake.tail) - 1]
        out = snake.y > height or snake.y < 0 or snake.x > width or snake.x < 0
        if collision or out:
            break

        if (snake.size / numFrames < .001):
            break

    return numFrames + snake.size* 5



#Assumes the network has an input layer of 5 neurons
def playWithNet(network):
    snake = Snake()
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    #clock = pygame.time.Clock()

    if len(network.layers[0].neurons) != 5:
        raise Exception("There are not 5 input neurons!")

    if len(network.layers[-1].neurons) != 4:
        raise Exception("There are not 4 output neurons!")

    inputs = []
    for n in network.layers[0].neurons:
        inputs.append(n.connections[0].parent)

    inputDict = {"size":inputs[0], "snakeX":inputs[1], "snakeY":inputs[2], "foodX":inputs[3], "foodY":inputs[4]}
    numFrames = 0
    badMoves = 0


    while True:

        numFrames+=1
        #clock.tick(30)
        pygame.event.get()

        for event in pygame.event.get():  # wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        snake.move()


        #Get output from neural network
        nValues = []

        for n in network.layers[-1].neurons:
            nValues.append(n.value)

        maxVal = max(nValues)
        index = nValues.index(maxVal)

        if index == 0 and snake.direction != direction.Down:
            snake.direction = direction.Up

        elif index == 1 and snake.direction != direction.Left:
            snake.direction = direction.Right

        elif index == 2 and snake.direction != direction.Up:
            snake.direction = direction.Down

        elif index == 3 and snake.direction != direction.Right:
            snake.direction = direction.Left

        else:
            print("bad move")
            badMoves+=1


        #Give nerual net input and calculate new values

        inputDict["size"].value = snake.size
        inputDict["snakeX"].value = snake.x
        inputDict["snakeY"].value = snake.y
        inputDict["foodX"].value = foodLoc[0]
        inputDict["foodY"].value = foodLoc[1]

        network.runNetwork()


        screen.fill((0, 0, 0))

        for x in range(0, width, squareSize):
            pygame.draw.line(screen, (255, 255, 255), [x, 0], [x, height], 1)
            pygame.draw.line(screen, (255, 255, 255), [0, x], [width, x], 1)

        for t in snake.tail:
            pygame.draw.rect(screen, (0, 255, 255), [t[0], t[1], squareSize, squareSize])

        pygame.draw.rect(screen, (255, 0, 0), [foodLoc[0], foodLoc[1], squareSize, squareSize])

        pygame.display.flip()

        collision = [snake.x // squareSize * squareSize, snake.y // squareSize * squareSize] in snake.tail[
                                                                                                0:len(snake.tail) - 1]
        out = snake.y > height or snake.y < 0 or snake.x > width or snake.x < 0
        if collision or out:
            break


        if(snake.size / numFrames < .001):
            numFrames = -10
            break

    return 2 * snake.size / numFrames - badMoves




def playSnake():
    snake = Snake()
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()


    while True:

        clock.tick(30)
        pygame.event.get()
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():  # wait for events
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        snake.move()

        if keys[K_LEFT]:
            snake.direction = direction.Left
        elif keys[K_RIGHT]:
            snake.direction = direction.Right
        elif keys[K_UP]:
            snake.direction = direction.Up
        elif keys[K_DOWN]:
            snake.direction = direction.Down



        screen.fill((0,0,0))

        for x in range(0, width, squareSize):
            pygame.draw.line(screen, (255, 255, 255), [x, 0], [x, height], 1)
            pygame.draw.line(screen, (255, 255, 255), [0, x], [width, x], 1)


        for t in snake.tail:

            pygame.draw.rect(screen, (0,255,255), [t[0], t[1], squareSize, squareSize])

        pygame.draw.rect(screen, (255,0,0), [foodLoc[0], foodLoc[1], squareSize, squareSize])

        pygame.display.flip()

        collision = [snake.x // squareSize * squareSize, snake.y // squareSize * squareSize] in snake.tail[
                                                                                                    0:len(snake.tail) - 2]
        out = snake.y > height or snake.y < 0 or snake.x > width or snake.x < 0
        if collision or out:
            lose()
