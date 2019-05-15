from snake import *
from neat import *
from copy import deepcopy



population = 500
generations = 500


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


def breedNet(n1, n2, c):
    for i in range(len(n1.layers)):
        for j in range(len(n1.layers[i].neurons)):

            bias1 = n1.layers[i].neurons[j].bias
            bias2 = n2.layers[i].neurons[j].bias

            r1 = randint(0, 1)
            if (r1 == 0):
                bias = bias1
            else:
                bias = bias2

            r1 = randint(0, 10)
            r2 = randint(0, 10)

            if r1 == 0:
                bias += .001 * randint(1, 1000)
            if r2 == 0:
                bias -= .001 * randint(1, 1000)

            c.layers[i].neurons[j].bias = bias



            for k in range(len(n1.layers[i].neurons[j].connections)):
                weight1 = n1.layers[i].neurons[j].connections[k].weight
                weight2 = n2.layers[i].neurons[j].connections[k].weight

                r1 = randint(0,1)
                if(r1 == 0):
                    weight = weight1
                else:
                    weight = weight2



                r1 = randint(0,10)
                r2 = randint(0,10)

                if r1 == 0:
                    weight += .001 * randint(1, 1000)
                if r2 == 0:
                    weight -= .001 * randint(1, 1000)


                c.layers[i].neurons[j].connections[k].weight = weight



probTable = []
num = population // 10
for x in range(0,population // 10):
    for y in range(0,num):
        probTable.append(x)

    num-=1






nets = []

for x in range(population):
    nets.append(genRandNet(5,4,[4,4], [5,5], [-5,5], [5,5]))

for x in range(generations):
    print("Generation: " + str(x))
    for net in nets:

        net.fitness = playWithNetHeadLess(net)


    nets.sort(key=lambda x: x.fitness, reverse=True)
    best = deepcopy(nets[0:population// 10])

    for n in nets:
        p1 = best[probTable[randint(0, len(probTable) - 1)]]
        p2 = best[probTable[randint(0, len(probTable) - 1)]]

        breedNet(p1,p2,n)

while(1):
    for n in best[0:3]:
        playWithNet(n)



