import numpy as np
import scipy.stats as stats
import pylab as pl

data_avg = []
data_max = []
data_sim = []
# tested for avg max sim
# tuple = (win rate, p) * tested
with open('popular_results.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        line = list(map(float, line))
        avg, avgp, maxi, maxip, sim, simp = line
        data_avg.append(avg*100)
        data_max.append(maxi*100)
        data_sim.append(sim*100)


def normal_distribution(data):
    data = sorted(data)
    fit = stats.norm.pdf(data, np.mean(data), np.std(data))
    pl.plot(data, fit, '-o')
    pl.hist(data, density=True)
    pl.show()


for data in [data_avg, data_max, data_sim]:
    normal_distribution(data)

# data_avg = sorted(data_avg)
#
# fit = stats.norm.pdf(data_avg, np.mean(data_avg), np.std(data_avg))
#
# pl.plot(data_avg, fit, '-o')
# pl.hist(data_avg, density=True)
# print("for avg")
# pl.show()
#
#
# data_max = sorted(data_max)
# fit = stats.norm.pdf(data_max, np.mean(data_max), np.std(data_max))
#
# pl.plot(data_max, fit, '-o')
# pl.hist(data_max, density=True)
# print("for max")
# pl.show()
#
#
# data_sim = sorted(data_sim)
# fit = stats.norm.pdf(data_sim, np.mean(data_sim), np.std(data_sim))
#
# pl.plot(data_max, fit, '-o')
# pl.hist(data_max, density=True)
# print("for max")
# pl.show()
