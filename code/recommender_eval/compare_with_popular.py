import pickle
import numpy as np
import pandas as pd
from code.recommender_eval.recommendations import *
from code.recommender_eval.tests_math import *
import time
from scipy import stats

# TODO simple version - no keeping track of watched
# TODO pain in the ass version - keep track of watched
start = time.time()
CHUNK_SIZE = 300_000
MOVIE_SAMPLE = 0.2
USER_SAMPLE = 0.0005 * 2
SAMPLE = 5
user_path = '/home/natosath/Desktop/Projekt/code/user/pickle_test.pkl'
all_movies_path = '/home/natosath/Desktop/Projekt/code/database.csv'
matrix_path = '/home/natosath/Desktop/Projekt/code/matrix.csv'

all_movies = pd.read_csv(all_movies_path, usecols=["tconst", "genres"])
sample_movies = all_movies.head(6000)
# sample_movies = np.array_split(all_movies, 3)[0]
matrix = pd.read_csv(matrix_path, usecols=["tconst", "similarity", "movie"])

with open(user_path, 'rb') as file:
    users = pickle.load(file)

key_max = int(max(users.keys()) * USER_SAMPLE)
users = {k: v for k, v in users.items() if k < key_max}

# 0 is me, 1 is random
wins = {0: 0, 1: 0}


def compare_recommenders(series, user_data):
    # print(user_data)
    popular = sample_movies.head(10)
    similar = get_recommendations(matrix, series)
    if similar.empty:
        print("empty", series.tconst)
        return
    similar = similar.merge(all_movies, how="inner")  # get genres for the movie
    rez = get_winner(series, popular, similar, user_data)
    # print(similar)
    wins[rez] += 1


for user_id, user_data in users.items():
    watched = sample_movies.sample(n=SAMPLE)
    watched.apply(func=compare_recommenders, axis=1, args={user_data})

# take 5 films and declare them watched
# for each film recommend 10 films from each system
# from our/my system take the most similar
# for the random system take 10 random films
# compare how many films are more relevant for the user
# compare the genres
# might have to min-hash them
#   for the min-hash, create script which will
#   create and pickle a dict with which to min hash it
print("my recommender won: ", wins[0], "times out of ", wins[0] + wins[1])
print("p is: ", stats.binom_test(wins[0], wins[0] + wins[1], p=0.5))
print("done in ", time.time() - start, " seconds for ", key_max, " users")
print("done in ", (time.time() - start) / 60, " minutes")
