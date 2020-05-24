import pickle
import numpy as np
import pandas as pd
import time

# TODO simple version - no keeping track of watched
# TODO pain in the ass version - keep track of watched
start = time.time()
CHUNK_SIZE = 300_000
MOVIE_SAMPLE = 0.2
USER_SAMPLE = 0.001
SAMPLE = 5
user_path = '/home/natosath/Desktop/Projekt/code/user/pickle_test.pkl'
all_movies_path = '/home/natosath/Desktop/Projekt/code/database.csv'
matrix_path = '/home/natosath/Desktop/Projekt/code/matrix.csv'

all_movies = pd.read_csv(all_movies_path, usecols=["tconst", "genres"])
all_movies = np.array_split(all_movies, int(1 / MOVIE_SAMPLE))[0]
matrix = pd.read_csv(matrix_path, usecols=["tconst", "similarity", "movie"])
tconst = matrix.groupby('tconst').nunique()
movie = matrix.groupby('movie').nunique()
print(tconst)
print(movie)
