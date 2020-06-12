import numpy as np
import scipy.stats as stats
import pylab as pl

data = []

with open('filter_data.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        reduction = 1 - (int(line[1]) / int(line[0]))
        data.append(reduction * 100)

data = sorted(data)

fit = stats.norm.pdf(data, np.mean(data), np.std(data))

pl.plot(data, fit, '-o')
pl.hist(data, density=True)
pl.show()

