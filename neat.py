from random import randint
import math
import tkinter as tk
from random import uniform
from copy import deepcopy
from math import tanh


test = []

def sigmoid(x):

    try:
        #ret = 1/(1+math.exp((-1*x)))
        ret = tanh(float(x))

    except Exception as e:
        print("There was a problem with the sigmoid")
        print(x)
        print(e)


    return ret




class Connection():

    def __init__(self, n1, weight):
        self.parent = n1
        self.weight = weight





class Neuron():

    def __init__(self, bias, input = False):

        self.connections = []
        self.value = 0
        self.input = input
        self.bias = bias


    def calculate(self):

        if self.input:
            self.value = self.connections[0].parent.getInput() * self.connections[0].weight
        else:

            self.value = 0
            for connection in self.connections:
                self.value = (connection.parent.value * connection.weight) + self.value
                #print(self.value)
        self.value+=self.bias
        self.value = sigmoid(self.value)





class Layer():


    def __init__(self, neurons=[]):
        self.neurons = neurons


    def calculate(self):
        for neuron in self.neurons:
            neuron.calculate()

class Input():

    def __init__(self):
        self.value = -1



    def getInputR(self):
        x = randint(1,10)
        test.append(x)
        #print(x)
        return x

    def getInput(self):
        return self.value


class Network():

    def __init__(self, layers=[]):
        self.layers = layers
        self.fitness = -1

        self.inputs = []
        self.outputs = []

    def checkEquality(self, n2):
        for i in range(len(self.layers)):
            for j in range(len(self.layers[i].neurons)):

                bias1 = self.layers[i].neurons[j].bias
                bias2 = n2.layers[i].neurons[j].bias

                if bias1 != bias2:
                    return False

                for k in range(len(self.layers[i].neurons[j].connections)):
                    weight1 = self.layers[i].neurons[j].connections[k].weight
                    weight2 = n2.layers[i].neurons[j].connections[k].weight

                    if weight1 != weight2:
                        return False

        return True


    def runNetwork(self):


        for layer in self.layers:
            layer.calculate()



        result = []
        for neuron in self.layers[-1].neurons:
            result.append(neuron.value)

        return result


#layer range is the a 2 element list that has the min and max numbers of layers
#The min number really needs to be greater than 2 otherwise it is kind of useless
#Same with nueronRange but min needs to be 1
#Input and output need to stay constant
def getNeuronIndex(net, neur):

    x = -1
    y = -1

    for layer in net.layers:
        x+=1
        for neuron in layer.neurons:
            y+=1
            if neuron == neur:
                return [x,y]

        y = -1

    raise Exception("did not find neuron")


def visualizeNet(network):
    root = tk.Tk()
    canvas = tk.Canvas(root, width=1000, height=500)
    canvas.pack()

    size = 50
    cursor = [0,0]

    for layer in network.layers:

        for n in layer.neurons:
            canvas.create_oval(cursor[0], cursor[1],cursor[0]+size, cursor[1]+size )
            cursor[1]+=size*2

        cursor[0]+=size*2
        cursor[1] = 0

    baseX = size/2
    baseY = size/2
    color = "red"
    for i in range(1,len(network.layers)):

        if color == "red":
            color = "blue"
        else:
            color = "red"

        for j in range( len(network.layers[i].neurons)):

            cursor =  [baseX + size * i * 2, baseY + size * j * 2]

            for c in network.layers[i].neurons[j].connections:
                pCursor = getNeuronIndex(network, c.parent)
                pCursor[0] = baseX + size * pCursor[0] * 2
                pCursor[1] = baseY + size * pCursor[1] * 2
                canvas.create_line(cursor[0], cursor[1], pCursor[0], pCursor[1], fill=color)


    baseX = baseX + (len(network.layers) + 4) * size
    baseY = 10
    for i in range(0, len(network.layers)):

        if color == "red":
            color = "blue"
        else:
            color = "red"

        for j in range(len(network.layers[i].neurons)):

            cursor = [baseX + size * i * 2, baseY + size * j * 2]
            canvas.create_text(cursor[0], cursor[1], text=str(network.layers[i].neurons[j].bias)[0:8])
            cursor[1] += 15
            for c in network.layers[i].neurons[j].connections:
                canvas.create_text(cursor[0], cursor[1], text=str(c.weight)[0:8])
                cursor[1] += 12








    root.update()



def genRandNet(numInputs, numOutputs, layerRange, neuronRange,connectionRange):

    network = Network()
    layers = []

    numLayers = randint(layerRange[0], layerRange[1])

    for x in range(numLayers):

        neurons = []

        if x == 0:
            numNeurons = numInputs
        elif x == numLayers -1:
            numNeurons = numOutputs
        else:
            numNeurons = randint(neuronRange[0], neuronRange[1])
        for y in range(numNeurons):
            if(x == 0):
                neurons.append(Neuron( uniform(-1,1),input=True))
            else:
                neurons.append(Neuron( uniform(-1,1)))

        layers.append(Layer(neurons=deepcopy(neurons)))
    network.layers = layers


    #setup input layer to randint
    for n in network.layers[0].neurons:
        n.connections = [ Connection(Input(), uniform(-1,1)  ) ]
        network.inputs.append(n.connections[0].parent)




    #setup the rest of the layers
    for x in range(1,numLayers):
        childLayer = network.layers[x]
        parentLayer = network.layers[x-1]

        numParentNeurons = len(parentLayer.neurons)


        for n in childLayer.neurons:
            numConnections = randint(connectionRange[0],connectionRange[1])

            if(numConnections > numParentNeurons):
                if(connectionRange[0] > numParentNeurons):
                    numConnections = randint(numParentNeurons, numParentNeurons)
                else:
                    numConnections = randint(connectionRange[0], numParentNeurons)


            usedParents = []
            for i in range(numConnections):
                rWeight = uniform(-1,1)

                #Does not allow repeated parents
                rParent = randint(0, numParentNeurons - 1)
                while(rParent in usedParents):
                    rParent = randint(0, numParentNeurons - 1)

                usedParents.append(rParent)

                n.connections.append( Connection(parentLayer.neurons[rParent], rWeight) )


    for x in range(len(network.layers[-1].neurons)):
        network.outputs.append(network.layers[-1].neurons[x])

    return network



















"""
#build and test manual net

in1 = Input()
in2 = Input()


n11 = Neuron(input=True)
n12 = Neuron(input=True)



n21 = Neuron()
n22 = Neuron()

n31 = Neuron()


n11.connections = [ Connection(in1, 3)]
n12.connections = [ Connection(in2, 5)]

n21.connections = [ Connection(n11, 4), Connection(n12, 7)]
n22.connections = [ Connection(n11,2), Connection(n12,3)]

n31.connections = [ Connection(n21,9), Connection(n22, 8) ]

layer1 = Layer([n11,n12])
layer2 = Layer([n21,n22])
layer3 = Layer([n31])


testNet = Network([layer1, layer2, layer3])


result = testNet.runNetwork()
print(result)
print(156 * test[0] + 435 * test[1])
"""


#numInputs, numOutputs, layer range, neuron range, weight range
#net = genRandNet(5, 4, [3,6], [3,6], [-5,5])
#visualizeNet(net)




