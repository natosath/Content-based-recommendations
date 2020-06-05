import pandas as pd
import numpy as np
import pickle
import time

start = time.time()
csv = pd.read_csv('gen_normed_np-database.csv')
print("csv read in: ", time.time() - start, " seconds")
csv.info()
start = time.time()
compressed = pd.read_pickle('gen_normed_np-database.zip')
print("zip read in: ", time.time() - start, " seconds")
compressed.info()
# zip read is about 10% slower
# zip read become about 20% slower after pycharm does some caching
