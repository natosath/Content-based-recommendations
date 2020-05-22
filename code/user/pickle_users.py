import pandas as pd
from code.user.simple_user import SimpleUser
import time
import pickle

CHUNK_SIZE = 300_000
start = time.time()
path_ratings = '/home/natosath/Desktop/Projekt/movie-lens-csv/my_ratings_imdb_id.csv'
path_database = '/home/natosath/Desktop/Projekt/code/database.csv'
ratings = pd.read_csv(path_ratings, chunksize=CHUNK_SIZE, low_memory=False)
database = pd.read_csv(path_database, usecols=["tconst", "genres"])
database.info(verbose=True)
users = dict()


def load_user(series):
    if series.userId not in users.keys():
        users[series.userId] = SimpleUser(int(series.userId))
    users[series.userId].update(series)


print("starting chunk")
for rating in ratings:
    rating = rating.merge(database)
    rating.apply(func=load_user, axis=1, args={})
    print("chunk done, ", time.time() - start, " seconds elapsed since start")
    # rating.info(verbose=True)
    print("num of users: ", len(users.keys()))
print("num of users: ", len(users.keys()))

print("pickling")
with open("pickle_test.pkl", "wb") as test:
    pickle.dump(users, test)

print("unpickling")
with open("pickle_test.pkl", "rb") as test:
    users = pickle.load(test)
print("max user id", max(users.keys()))
# print(users)

print(time.time() - start, " seconds")
print((time.time() - start) / 60, " minutes")
print((time.time() - start) / 3600, " hours")
