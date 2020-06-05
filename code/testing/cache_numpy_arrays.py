import numpy as np

cache = [np.zeros(x) for x in range(1, 6 + 1)]
test = {x: np.zeros(x) for x in range(1, 6 + 1)}
print(cache)
print(test)