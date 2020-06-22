import pandas as pd
import warnings
import time

start = time.time()
# warning is suppressed because it is caused by numpy and vanilla python
# type disagreement
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('my_ratings_imdb_id.csv', index_col=0)
df = df.sort_values(by='userId')
df = df.reset_index(drop=True)
df.to_csv('sorted_rating_with_imdb_id.csv')
# print(max(df["userId"]))
print("time: ", time.time() - start)
