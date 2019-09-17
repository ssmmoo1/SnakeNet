from enum import Enum
from random import randint
from gaTools import Simulation, breedType
import time
from snake import playWithNet
from random import random


#Configurations
configs = {
    "savePath":"F:/Documents/PythonProjects/snakeNet/savedSnakes",
    "saveFolderName":"training",

    "population": 250,
    "generations": 5000,

    "numInputs": 8,
    "numOutputs": 4,

    "maxLayers": 4,
    "minLayers": 4,

    "maxNeurons": 12,
    "minNeurons": 12,

    "maxConnections": 16,
    "minConnections": 16,

    "mutationRate": .02,
    "breedFunction": breedType.mutateOnly,

    "headless": False,
    "slow": False,
    }



def getFitness(net, seed):
    return playWithNet(net,rseed=seed,headless=configs["headless"], slow=configs["slow"])
evolution = Simulation(configs,getFitness)
evolution.runSimulation()

