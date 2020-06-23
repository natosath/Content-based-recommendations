from sklearn.metrics.pairwise import cosine_similarity
import time
import numpy as np
import numpy.linalg as linalg

start = time.time()

x = np.ones(6)
y = np.array([1, 0.67, 0.5, 0, 0.5, 1])
z = np.array([1, 0, 0.5, 0.2, 0.5, 0])

# for i in range(2000):
#     print(np.dot(x, y)/(linalg.norm(x) * linalg.norm(y)))
#     print(np.dot(x, z)/(linalg.norm(x) * linalg.norm(z)))

print((z-1)*-1)

print(time.time() - start, "seconds")
