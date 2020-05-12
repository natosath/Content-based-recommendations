import numpy as np
import time
from numba import vectorize, cuda, numba

a = [[1, 2, 3],
     [3, 2, 1],
     [2, 1, 3]] * 100
b = [[1, 3, 3],
     [6, 2, 5],
     [1, 4, 3]] * 100

N = 1_000


@vectorize(['float32(float32, float32)'], target='cuda')
def add(x, y):
    return x + y


x = np.array(a, dtype=np.float32)
y = np.array(b, dtype=x.dtype)


@numba.jit
def gpu():
    # gpu_start = time.time()
    for i in range(0, N):
        c = add(x, y)
    # print("using GPU: ", time.time() - gpu_start)


def cpu():
    cpu_start = time.time()
    for i in range(0, N):
        c = x + y
    print("using CPU: ", time.time() - cpu_start)


gpu()
cpu()
