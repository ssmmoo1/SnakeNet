from enum import Enum
from neat import *
from copy import deepcopy
from random import uniform
import saveFileTools
import time
from pickle import dump


class breedType(Enum):
    averaging = 0
    swapping = 1
    mutateOnly = 2

class Simulation():

    def __init__(self, configs, fitnessFunc):

        self.configs = configs
        self.fitnessFunc = fitnessFunc
        self.best = []


    def mutateNet(self, n):
        for i in range(len(n.layers)):
            for j in range(len(n.layers[i].neurons)):

                r1 = randint(1, 1//self.configs["mutationRate"])

                if r1 == 1:
                    delta = uniform(-1, 1)

                    n.layers[i].neurons[j].bias += delta

                for k in range(len(n.layers[i].neurons[j].connections)):
                    r1 = randint(1, 1//self.configs["mutationRate"])

                    if r1 == 1:
                        delta = uniform(-1, 1)
                        n.layers[i].neurons[j].connections[k].weight += delta

    #Swapping breeding algorithm
    def breedNetS(self,n1, n2, c):
        for i in range(len(n1.layers)):
            for j in range(len(n1.layers[i].neurons)):

                bias1 = n1.layers[i].neurons[j].bias
                bias2 = n2.layers[i].neurons[j].bias

                r1 = randint(0,1)
                if (r1 == 0):
                    bias = bias1
                else:
                    bias = bias2

                r1 = randint(1, 1 // self.configs["mutationRate"])

                if r1 == 1:
                    bias += uniform(-1, 1)

                c.layers[i].neurons[j].bias = bias

                for k in range(len(n1.layers[i].neurons[j].connections)):
                    weight1 = n1.layers[i].neurons[j].connections[k].weight
                    weight2 = n2.layers[i].neurons[j].connections[k].weight

                    r1 = randint(0, 1)
                    if (r1 == 0):
                        weight = weight1
                    else:
                        weight = weight2

                    r1 = randint(1, 1 // self.configs["mutationRate"])

                    if r1 == 1:
                        weight += uniform(-1, 1)

                    c.layers[i].neurons[j].connections[k].weight = weight

    #Averaging breed algorithm
    def breedNetA(self,n1, n2, c):
        for i in range(len(n1.layers)):
            for j in range(len(n1.layers[i].neurons)):

                bias1 = n1.layers[i].neurons[j].bias
                bias2 = n2.layers[i].neurons[j].bias

                bias = (bias1 + bias2) / 2

                r1 = randint(1, 1 // self.configs["mutationRate"])

                if r1 == 1:
                    bias += uniform(-1, 1)

                c.layers[i].neurons[j].bias = bias

                for k in range(len(n1.layers[i].neurons[j].connections)):
                    weight1 = n1.layers[i].neurons[j].connections[k].weight
                    weight2 = n2.layers[i].neurons[j].connections[k].weight

                    weight = (weight1 + weight2) / 2

                    r1 = randint(1, 1 // self.configs["mutationRate"])

                    if r1 == 1:
                        weight += uniform(-1, 1)

                    c.layers[i].neurons[j].connections[k].weight = weight
    '''

    def breedNetA(self,n1, n2, c):
        for i in range(len(n1.layers)):
            for j in range(len(n1.layers[i].neurons)):

                avg = (n1.layers[i].neurons[j].bias + n2.layers[i].neurons[j].bias) / 2

                r1 = randint(0, 10)
                r2 = randint(0, 10)

                if r1 == 0:
                    avg += .001 * randint(1, 10000)
                if r2 == 0:
                    avg -= .001 * randint(1, 10000)

                c.layers[i].neurons[j].bias = avg

                for k in range(len(n1.layers[i].neurons[j].connections)):
                    weight1 = n1.layers[i].neurons[j].connections[k].weight
                    weight2 = n2.layers[i].neurons[j].connections[k].weight

                    avg = (weight1 + weight2) / 2
                    r1 = randint(0, 10)
                    r2 = randint(0, 10)

                    if r1 == 0:
                        avg += .001 * randint(1, 10000)
                    if r2 == 0:
                        avg -= .001 * randint(1, 10000)

                    c.layers[i].neurons[j].connections[k].weight = avg
    '''
    def checkAllEquality(self, nets):
        numEqual = 0
        for x in range(len(nets)):
            for y in range(len(nets)):
                if x == y:
                    continue

                if nets[x].checkEquality(nets[y]):
                    numEqual+=1

        print("****** Number of equivalent networks " + str(numEqual))

        if numEqual != 0:

            raise Exception("Equal networks")


    def runSimulation(self):

        path = saveFileTools.setupFolder('F:/Documents/PythonProjects/snakeNet/savedSnakes', 'training')
        configFile = open(path + "/configFile.txt", "w+")
        configFile.write(str(self.configs))
        configFile.close()

        probTable = []
        num = self.configs["population"] // 10
        for x in range(0, self.configs["population"] // 10):
            for y in range(0, num):
                probTable.append(x)

            num -= 3

        print(probTable)

        nets = []
        highestFitness = -1
        for x in range(self.configs["population"]):
            nets.append(genRandNet(self.configs["numInputs"], self.configs["numOutputs"],
                                   [self.configs["minLayers"], self.configs["maxLayers"]],
                                   [self.configs["minNeurons"], self.configs["maxNeurons"]],
                                   [self.configs["minConnections"], self.configs["maxConnections"]]))
            #visualizeNet(nets[x])

        #self.checkAllEquality(nets)
        seed = randint(0, 100000000)
        for x in range(self.configs["generations"]):
            print("Generation: " + str(x))

            for y in range(len(nets)):

                nets[y].fitness = self.fitnessFunc(nets[y],seed)

            nets.sort(key=lambda g: g.fitness, reverse=True)
            best = deepcopy(nets[0:self.configs["population"] // 10])
            if best[0].fitness > highestFitness:
                highestFitness = best[0].fitness

            print("Fitness best: " + str(best[0].fitness))
            print("Fitness worst: " + str(nets[-1].fitness))


            '''
            for z in range(1,len(nets)):
                nets[z] = deepcopy(nets[0])
                self.mutateNet(nets[z])
            '''

            for z in range(1, len(nets)):
                p1 = best[probTable[randint(0, len(probTable) - 1)]]
                p2 = best[probTable[randint(0, len(probTable) - 1)]]

                if(self.configs["breedFunction"] == breedType.averaging):
                    self.breedNetA(p1, p2, nets[z])

                elif(self.configs["breedFunction"] == breedType.swapping):
                    self.breedNetS(p1,p2,nets[z])

                elif(self.configs["breedFunction"] == breedType.mutateOnly):
                    nets[z] = deepcopy(p1)
                    self.mutateNet(nets[z])
                else:
                    raise Exception("Incorrect breeding function")
            #self.checkAllEquality(nets)

            for i in range(3):
                save = open(path + "/bestSnake" + str(i) + ".pickle", "wb")
                dump(best[i], save)
                save.close()

                if (best[i].fitness >= highestFitness):
                    save = open(path + "/bestSnakeRecord.pickle", "wb")
                    dump(best[i], save)
                    save.close()
                    #visualizeNet(best[i])

            graph = open(path + "/fitGraph.csv", "a+")
            graph.write(str(x) + "," + str(best[0].fitness) + "\n")
            graph.close()






