import pandas as pd
import numpy as np
import math
from collections import Counter
from code.user.simple_user import SimpleUser

# df = pd.read_csv('../new_database.csv', index_col=0)
# df["genres"] = df["genres"].str.lower()
# print(df["genres"])
vector = np.array([2., 2.5, 0., 6., 19., 12., 0., 40.5, 0., 4.5, 5., 0., 0., 0.,
                   9.5, 3.5, 3.5, 0., 0., 1., 0., 0.5, 0., 0., 0., 0.], dtype=float)
divide = np.array([1., 1., 0., 2., 9., 6., 0., 18., 0., 2., 1., 0., 0., 0., 4., 2., 2., 0.,
                   0., 1., 0., 1., 0., 0., 0., 0.], dtype=float)
# this is how to make 0 division return 0
print(np.divide(vector, divide, out=np.zeros_like(vector), where=divide != 0))
print(vector.sum())

# x = dict({'a': SimpleUser(1), 'b': SimpleUser(2), 'c': SimpleUser(3)})
# y = dict({'b': SimpleUser(3), 'c': SimpleUser(4), 'd': SimpleUser(5)})
# print({k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y)})

# print(np.average(vector))
# print(np.average(vector[vector != 0]))
