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


w_values = []
p_values = []
equals = 0
total = 0

with open('cosine_results.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        line = [float(x) for x in line]
        w_values.append(line[1])
        p_values.append(line[0])
        equals += line[2]
        total += 1
print(equals / total)

objects = ('iste vrijednosti', 'nisu iste vrijednosti')
y_pos = np.arange(len(objects))
performance = [equals, total]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Udio identičnih preporuka je %.4f' % (equals / total))
plt.show()

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija p-vrijednosti Studentovog t-testa')
normal_distribution(p_values)

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija p-vrijednosti Wilcoxonovog testa')
normal_distribution(w_values)
