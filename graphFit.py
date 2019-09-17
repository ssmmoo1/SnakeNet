import matplotlib.pyplot as plt
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
path = askopenfilename()

x = []
y = []

with open(path,'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.plot(x,y, label='Loaded from file!')
plt.xlabel('Generations')
plt.ylabel('Fitness')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()