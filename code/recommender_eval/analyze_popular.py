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


p_values = []
w_values = []
w_g_values = []
win_values = []
wins = 0
total = 0

with open('popular_results.txt', mode="r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip().split(" ")
        line = [float(x) for x in line]
        p_values.append(line[0])
        w_values.append(line[1])
        w_g_values.append(line[2])
        win_values.append(line[3])
        wins += line[3]
        total += 1
print(wins / total)

objects = ('broj "pobjeda"', 'sveukupni broj preporučivanja')
y_pos = np.arange(len(objects))
performance = [wins, total]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Udio pobjeda je %.4f' % (wins / total))
plt.show()

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija p-vrijednosti Studentovog t-testa')
normal_distribution(p_values)

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija p-vrijednosti Wilcoxonovog testa')
normal_distribution(w_values)

plt.ylabel('udio')
plt.xlabel('vrijednost')
plt.title('Distribucija p-vrijednosti Wilcoxonovog testa za hipotezu '
          'daje li sustav bolje preporuke od nasumičnog preporučitelja')
normal_distribution(w_g_values)

print("u ", len([p for p in p_values if p <= 0.05]) * 100 / len(p_values),
      "% slučajeva sigurni smo da performanse nisu iste u Studentovom t-testu")

print("u ", len([p for p in w_values if p <= 0.05]) * 100 / len(w_values),
      "% slučajeva sigurni smo da performanse nisu iste u Wilcoxonovom testu")

print("u ", len([p for p in w_g_values if p <= 0.05]) * 100 / len(w_g_values),
      "% slučajeva sigurni smo da je sustav bolji od nasumičnog po Wilcoxonovom testu")

print("n je ", total)

counter = 0
for p, win in zip(w_g_values, win_values):
    if win == 1 and p <= 0.05:
        counter += 1
print("sigurnih pobjeda ima: ", counter * 100 / len(p_values), " %")
