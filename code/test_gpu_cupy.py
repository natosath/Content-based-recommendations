import numpy as np
import cupy as cp
import time

a = [[1, 2, 3],
     [3, 2, 1],
     [2, 1, 3]] * 100
b = [[1, 3, 3],
     [6, 2, 5],
     [1, 4, 3]] * 100
first = ["lalal", "nm42", "hoho", "nm69", "nyeh"]
second = ["lalal", "nm42", "nm12", "nm69", "nyeh", "ne"]
third = ["lalal", "nm42", "hoho", "nm69", "nm99", "nm12", "zen"]


def similarity_numpy(prvi, drugi):
    prvi = np.array([item for item in prvi if "nm" in item])
    drugi = np.array([item for item in drugi if "nm" in item])
    prvi = np.array(prvi)
    drugi = np.array(drugi)
    intersect = np.intersect1d(prvi, drugi)
    print(intersect)
    rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    return rez


def similarity_cupy(prvi, drugi):
    # prvi = cp.array([item for item in prvi if "nm" in item])
    # drugi = cp.array([item for item in drugi if "nm" in item])
    prvi = cp.array(prvi, dtype=str)
    drugi = cp.array(drugi, dtype=str)
    sum = first + second
    # print(intersect)
    # rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    # return sum


def similarity_list(prvi, drugi):
    prvi = {item for item in prvi if "nm" in item}
    drugi = {item for item in drugi if "nm" in item}
    intersect = prvi & drugi
    print(intersect)
    rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    return rez
print(a)
print(b)

print("Numpy (CPU) : ")
np_start = time.time()
for i in range(0, 65000):
    prvi = np.array(a)
    drugi = np.array(b)
    treci = a + b
print("time: ", time.time() - np_start)
print("Cupy (GPU) : ")
cp_start = time.time()
for i in range(0, 65000):
    prvi = cp.array(a)
    drugi = cp.array(b)
    treci = a + b
print("time: ", time.time() - cp_start)
