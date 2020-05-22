import pickle
import numpy as np
import pandas as pd
from code.recommender_eval.recommendations import get_recommendations
import time

# TODO simple version - no keeping track of watched
# TODO pain in the ass version - keep track of watched
start = time.time()
CHUNK_SIZE = 300_000
MOVIE_SAMPLE = 0.1
USER_SAMPLE = 0.05
user_path = '/home/natosath/Desktop/Projekt/code/user/pickle_test.pkl'
all_movies_path = '/home/natosath/Desktop/Projekt/code/database.csv'
matrix_path = '/home/natosath/Desktop/Projekt/code/matrix.csv'

all_movies = pd.read_csv(all_movies_path, usecols=["tconst", "genres"])
all_movies = np.array_split(all_movies, int(1 / MOVIE_SAMPLE))[0]
all_movies.info(verbose=True)
matrix = pd.read_csv(matrix_path, usecols=["tconst", "similarity", "movie"], chunksize=CHUNK_SIZE)

with open(user_path, 'rb') as file:
    users = pickle.load(file)

key_max = int(max(users.keys()) * USER_SAMPLE)
users = {k: v for k, v in users.items() if k < key_max}

for user_id, user_data in users.items():
    watched = all_movies.sample(n=5)
    for movie in watched:
        from_random = all_movies.sample(n=5)
        from_my = get_recommendations(1, 2)
    # take 5 films and declare them watched
    # for each film recommend 10 films from each system
    # from our/my system take the most similar
    # for the random system take 10 random films

print("done in ", time.time() - start, " seconds")
print("done in ", (time.time() - start) / 60, " minutes")
