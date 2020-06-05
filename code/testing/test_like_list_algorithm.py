import numpy as np
import time
from scipy.spatial import distance

first = [11011, 696969, 420, 89, 30, 99]
second = [11011, 696969, 20, 89, 30, 9000]
third = [11011, 696969, 420, 89, 20, 7]
np_first = np.array(first)
np_second = np.array(second)
np_third = np.array(third)


# TODO try turning into numpy arrays
def similarity_set(x, y):
    # prvi = {item for item in x if "nm" in item}
    # drugi = {item for item in y if "nm" in item}
    prvi = set(x)
    drugi = set(y)
    intersect = prvi & drugi
    # print(intersect)
    rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    return rez


def similarity_numpy(x, y):
    rez = distance.jaccard(x, y)
    return 1 - rez


numpy_start = time.time()
for i in range(0, 66000):
    similarity_numpy(np_first, np_second)
    similarity_numpy(np_second, np_third)
numpy_duration = time.time() - numpy_start
print("numpy done")

list_start = time.time()
for i in range(0, 66000):
    similarity_set(third, first)
    similarity_set(second, third)
list_duration = time.time() - list_start
print("set done")

print("numpy time:", numpy_duration)
print("set time:", list_duration)
print("comparing returns numpy : set")
print(similarity_numpy(np_first, np_second), similarity_set(first, second))
print(similarity_numpy(np_second, np_second), similarity_set(second, second))
print(similarity_numpy(np_third, np_second), similarity_set(third, second))

# numpy lost!
# too much overhead in type conversion?
# first = [item for item in first if "nm" in item]
# second = [item for item in second if "nm" in item]
# print(first)
# print(second)
# print("or---")
# print(first or second)
# print(second or first)
# print("and---")
# print(first and second)
# print(second and first)

# first = ["lalal", "nm42", "hoho", "nm69", "nyeh"]
# second = ["lalal", "nm42", "nm12", "nm69", "nyeh", "ne"]
# third = ["lalal", "nm42", "hoho", "nm69", "nm99", "nm12", "zen"]
