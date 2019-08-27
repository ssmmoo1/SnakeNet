from snake import *
from neat import *
from copy import deepcopy
from random import uniform
from pickle import dump, load
from os import mkdir

population =300
generations =5000


""" Uses averaging did not work very well
def breedNet(n1, n2, c):
    for i in range(len(n1.layers)):
        for j in range(len(n1.layers[i].neurons)):

            avg = (n1.layers[i].neurons[j].bias + n2.layers[i].neurons[j].bias) / 2

            r1 = randint(0, 10)
            r2 = randint(0, 10)

            if r1 == 0:
                avg += .001 * randint(1,10000)
            if r2 == 0:
                avg -= .001 * randint(1,10000)

            c.layers[i].neurons[j].bias = avg

            for k in range(len(n1.layers[i].neurons[j].connections)):
                weight1 = n1.layers[i].neurons[j].connections[k].weight
                weight2 = n2.layers[i].neurons[j].connections[k].weight

                avg = (weight1 + weight2) / 2
                r1 = randint(0,10)
                r2 = randint(0,10)

                if r1 == 0:
                    avg += .001 * randint(1, 10000)
                if r2 == 0:
                    avg -= .001 * randint(1, 10000)


                c.layers[i].neurons[j].connections[k].weight = avg
"""



def breedNetB(n1, n2, c):
    for i in range(len(n1.layers)):
        for j in range(len(n1.layers[i].neurons)):

            bias1 = n1.layers[i].neurons[j].bias
            bias2 = n2.layers[i].neurons[j].bias

            r1 = randint(0, 1)
            if (r1 == 0):
                bias = bias1
            else:
                bias = bias2

            r1 = randint(0, 9)

            if r1 == 0:
                bias += uniform(-1,1)

            c.layers[i].neurons[j].bias = bias



            for k in range(len(n1.layers[i].neurons[j].connections)):
                weight1 = n1.layers[i].neurons[j].connections[k].weight
                weight2 = n2.layers[i].neurons[j].connections[k].weight

                r1 = randint(0,1)
                if(r1 == 0):
                    weight = weight1
                else:
                    weight = weight2



                r1 = randint(0,9)


                if r1 == 0:
                    weight += uniform(-1,1)



                c.layers[i].neurons[j].connections[k].weight = weight

def mutate(n):
    for i in range(len(n.layers)):
        for j in range(len(n.layers[i].neurons)):



            r1 = randint(0, 30)

            if r1 == 0:
                delta = uniform(-1,1)

                n.layers[i].neurons[j].bias += delta



            for k in range(len(n.layers[i].neurons[j].connections)):
                r1 = randint(0,30)

                if r1 == 0:
                    delta = uniform(-1,1)



                    n.layers[i].neurons[j].connections[k].weight += delta





def breedNetA(n1, n2, c):
    for i in range(len(n1.layers)):
        for j in range(len(n1.layers[i].neurons)):

            bias1 = n1.layers[i].neurons[j].bias
            bias2 = n2.layers[i].neurons[j].bias

            bias = (bias1 + bias2) / 2

            r1 = randint(0, 2)

            if r1 == 0:
                bias += uniform(-1,1)

            c.layers[i].neurons[j].bias = bias



            for k in range(len(n1.layers[i].neurons[j].connections)):
                weight1 = n1.layers[i].neurons[j].connections[k].weight
                weight2 = n2.layers[i].neurons[j].connections[k].weight

                weight = (weight1 + weight2) / 2



                r1 = randint(0,2)


                if r1 == 0:
                    weight += uniform(-1,1)



                c.layers[i].neurons[j].connections[k].weight = weight

id = randint(0,1000)
mkdir("Training" + str(id))
probTable = []
num = population // 10
for x in range(0,population//10):
    for i in range(0,num):
        probTable.append(x)

    num-=3





netIn = 12
nets = []
highestFit = 0
for x in range(population):
    nets.append(genRandNet(netIn,4,[3,3], [12,12], [16,16]))

for x in range(generations):
    print("Generation: " + str(x))

    seed = randint(0,19999)

    for i in range(len(nets)):

        nets[i].fitness = playWithNet(nets[i],seed, headless=True, slow=False)


    nets.sort(key=lambda i: i.fitness, reverse=True)
    best = deepcopy(nets[0:population// 10])



    for i in range(0,len(nets)):
        p1 = best[probTable[randint(0, len(probTable) - 1)]]
        p2 = best[probTable[randint(0, len(probTable) - 1)]]
        nets[i] = deepcopy(p1)
        mutate(nets[i])


    print("Fitness: " + str(best[0].fitness))
    for i in range(3):
        save = open("Training" + str(id) + "/bestSnake" + str(i) + ".pickle", "wb")
        dump(best[i], save)
        save.close()

        if(best[i].fitness > highestFit):
            save = open("Training" + str(id) + "/bestSnakeMAX.pickle", "wb")
            dump(best[i], save)
            save.close()

    graph = open("Training" + str(id) + "/fitGraph.csv", "a+")
    graph.write(str(x) + "," + str(best[0].fitness) + "\n")
    graph.close()

print("DONE")






