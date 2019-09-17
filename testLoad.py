from pickle import load
from snake import playWithNet
from random import randint
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from neat import *
from time import sleep
Tk().withdraw()
path = askopenfilename()
print(path)
file = open(path, 'rb')
snakenet = load(file)
#visualizeNet(snakenet)
while 1:


    print(playWithNet(snakenet, 1,headless=False, slow=False))
    sleep(1)