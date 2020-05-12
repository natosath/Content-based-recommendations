import random

import pandas as pd
from multiprocessing import Process
import time


def print_head(df, i):
    df = df.sort_values(by=["tconst"])
    x = 0
    for j in range(100000000):
        x *= x
        x += x
        x -= x
        x /= (j+1)
    print(i)
    # time.sleep(random.randint(0, 4) / 100)


if __name__ == '__main__':

    dfs = []
    procs = []
    N = 4

    for i in range(N):
        dfs.append(pd.read_csv('database.csv'))

    for i in range(N):
        p = Process(target=print_head, args=(dfs[i], i,))
        procs.append(p)
        p.start()
    # procs.reverse()
    for pro in procs:
        pro.join()
