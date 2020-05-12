import numpy as np
import time

first = ["lalal", "nm42", "hoho", "nm69", "nyeh"]
second = ["lalal", "nm42", "nm12", "nm69", "nyeh", "ne"]
third = ["lalal", "nm42", "hoho", "nm69", "nm99", "nm12", "zen"]


# TODO try turning into numpy arrays
def similarity_numpy(prvi, drugi):
    prvi = {item for item in prvi if "nm" in item}
    drugi = {item for item in drugi if "nm" in item}
    # prvi = np.array([item for item in prvi if "nm" in item])
    # drugi = np.array([item for item in drugi if "nm" in item])
    # prvi = np.array(prvi)
    # drugi = np.array(drugi)
    intersect = prvi & drugi
    print(intersect)
    rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    return rez


def similarity_list(prvi, drugi):
    prvi = [item for item in prvi if "nm" in item]
    drugi = [item for item in drugi if "nm" in item]
    intersect = set(prvi).intersection(drugi)
    print(intersect)
    rez = float(len(intersect) / (len(prvi) + len(drugi) - len(intersect)))
    return rez


# list_start = time.time()
# for i in range(0, 66000):
#     similarity_list(first, second)
#     similarity_list(second, third)
# list_duration = time.time() - list_start
# print("list done")
#
# numpy_start = time.time()
# for i in range(0, 66000):
#     similarity_numpy(third, first)
#     similarity_numpy(second, third)
# numpy_duration = time.time() - numpy_start
# print("numpy done")
# print("list time:", list_duration)
# print("numpy time:", numpy_duration)

print(similarity_list(first, second), similarity_numpy(first, second))
print(similarity_list(second, second), similarity_numpy(second, second))
print(similarity_list(third, second), similarity_numpy(third, second))

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
