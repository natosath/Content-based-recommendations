import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pylab as pl
import statistics


def normal_distribution(data):
    data = sorted(data)
    fit = stats.norm.pdf(data, np.mean(data), np.std(data))
    pl.plot(data, fit, '-o')
    pl.hist(data, density=True)
    pl.show()


genres = []
pojave = []
udio = []

with open('genre_data.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        genres.append(str(line[0]))
        pojave.append(float(line[1]))
        udio.append(float(line[2]))

objects = tuple(genres)
y_pos = np.arange(len(objects))
performance = udio
plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.ylabel('')
plt.xlabel('Udio u %')
plt.title('Udio žanrova u filmovima')
plt.show()

objects = tuple(genres)
y_pos = np.arange(len(objects))
performance = pojave
plt.barh(y_pos, performance, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.ylabel('Broj filmova sa tim žanrom')
plt.xlabel('Broj filmova')
plt.title('Zastupljenost žanrova')
plt.show()

zastupljenost = [648, 2004, 4848]
legenda = [1, 2, 3]

objects = tuple(legenda)
y_pos = np.arange(len(objects))
performance = zastupljenost
plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Broj filmova')
plt.xlabel('Broj žanrova')
plt.title('Broj filmova po broju žanrova')
plt.show()
