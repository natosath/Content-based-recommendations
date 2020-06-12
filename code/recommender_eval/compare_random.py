import pandas as pd
import numpy as np
import multiprocessing as mp
import pickle
import time
from code.recommender_eval import recommenders
import random
from scipy import stats

start = time.time()


# ako se poziva izvana dodaj suparnicki sustav kao parametar

# putanja do user picklea
# ucitaj usere i spremi nasumicnih 10-1000
# opt, kod multiprocessinga sa np.array_split podjeli na radnike
#   i jednog koji ce prikupljati rezultate
# za svakog usera odaberi jedan nasumicni film
#   iz uzmi jedan iz watched list
# posalji korisnika i film svom sustavu i protivnickom
# usporedi rezultat i biljezi win/lose
# izracunaj sign test
#   opt kod mp bi ovo napravio zasebni radnik

def convert_to_numpy(series):
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


SAMPLE = 7500
USERS = '../user/simple_users.pkl'
database = pd.read_csv('../vectorise_database/gen_normed_np-database.csv', usecols=["tconst", "genres"])
matrix = pd.read_csv('../new_matrix.csv')
sample = list(database.tconst.values)[0:SAMPLE]  # list of movie ids

n = 200
count = 0
users = []

file = open(USERS, mode="rb")
while 1:
    try:
        user = pickle.load(file)
        if random.randint(0, 5) == 0:
            users.append(user)
            count += 1
    except EOFError:
        break
    if count >= n:
        break
file.close()

# fit = []
better_avg = {"win": 0, "total": 0}
better_max = {"win": 0, "total": 0}
better_sim = {"win": 0, "total": 0}
for user in users:
    # comparing with random recommender
    # movie = random.choice(sample)
    movie = database.head(7500).sample(n=1)
    # print(movie)

    my_recommended = recommenders.my_recommender(user, movie, database, matrix)
    random_recommended = recommenders.random_recommender(user, movie, database, matrix)
    # print(my_recommended, random_recommended)

    # print(my_recommended)
    my_recommended["genres"] = my_recommended.genres.apply(func=convert_to_numpy)
    random_recommended["genres"] = random_recommended.genres.apply(func=convert_to_numpy)
    movie["genres"] = movie.genres.apply(func=convert_to_numpy)

    # print(my_recommended)
    my_recommended = recommenders.add_eval_columns(user, movie, my_recommended)
    random_recommended = recommenders.add_eval_columns(user, movie, random_recommended)

    # print(my_recommended["sim"])
    # print(random_recommended["sim"])

    if my_recommended["avg"].mean() > random_recommended["avg"].mean():
        better_avg["win"] += 1

    if my_recommended["avg"].max() > random_recommended["avg"].max():
        better_max["win"] += 1

    if my_recommended["sim"].mean() > random_recommended["sim"].mean():
        better_sim["win"] += 1

    better_avg["total"] += 1
    better_max["total"] += 1
    better_sim["total"] += 1

    # if my_recommended["avg"].max() > random_recommended["avg"].max():
    #     score["win"] += 1
    # score["total"] += 1

# print(better_avg["win"] / better_avg["total"])
# print("p for avg: ", stats.binom_test(better_avg["win"], better_avg["total"], p=0.5))
# print(better_max["win"] / better_max["total"])
# print("p for max: ", stats.binom_test(better_max["win"], better_max["total"], p=0.5))
# print(better_sim["win"] / better_sim["total"])
# print("p for sim: ", stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
# print("duration ", time.time() - start, " seconds")

# analysis output

print(better_avg["win"] / better_avg["total"], end=" ")
print(stats.binom_test(better_avg["win"], better_avg["total"], p=0.5), end=" ")
print(better_max["win"] / better_max["total"], end=" ")
print(stats.binom_test(better_max["win"], better_max["total"], p=0.5), end=" ")
print(better_sim["win"] / better_sim["total"], end=" ")
print(stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
