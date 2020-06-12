import pandas as pd
from code.user.simple_user import SimpleUser
import time

CHUNK_SIZE = 100_000
start = time.time()
path_ratings = '/home/natosath/Desktop/Projekt/movie-lens-csv/my_ratings_imdb_id.csv'
path_database = '/home/natosath/Desktop/Projekt/code/database.csv'
ratings = pd.read_csv(path_ratings, chunksize=CHUNK_SIZE, low_memory=False)
database = pd.read_csv(path_database, usecols=["tconst", "genres"])
users = dict()


def load_user(series):
    if series.userId not in users.keys():
        users[series.userId] = SimpleUser(int(series.userId))
    users[series.userId].update(series)


# TODO study how to pickle
# users need to be pickled
for chunk in ratings:
    print("starting chunk")
    chunk.apply(func=load_user, axis=1, args={})
    print("chunk done, ", time.time() - start, " seconds elapsed since start")
    print("num of users: ", len(users.keys()))
print(time.time() - start, " seconds")
