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


rmse = []
p_values = []
values = []

with open('new_rating_prediction_data.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        line = [float(x) for x in line]
        rmse.append(line[0])
        p_values.append(line[1])
        values.append(line[2])

plt.plot(values)
plt.ylabel('Broj ocjena')
plt.xlabel('Pokus')
plt.title("Broj ocjena u pokusima za n = 500 korisnika")
plt.show()

plt.plot(sorted(values))
plt.ylabel('Broj ocjena')
plt.xlabel('Pokus')
plt.title("Broj ocjena u pokusima za n = 500 korisnika, sortirano")
plt.show()

# for data in [rmse, p_values]:
#     normal_distribution(data)

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija RMSE vrijednosti za test skup')
normal_distribution(rmse)

plt.ylabel('udio')
plt.xlabel('p-vrijednost')
plt.title('Distribucija p-vrijednosti Studentovog t-testa prilikom računanja RMSE za testni skup')
normal_distribution(p_values)

print(statistics.mean(rmse))
