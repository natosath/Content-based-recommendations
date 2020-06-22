import pandas as pd
import numpy as np
import multiprocessing as mp
import pickle
import time

from pandas.core.common import SettingWithCopyWarning

from code.recommender_eval import recommenders
import random
import warnings
from scipy import stats


def convert_to_numpy(series):
    if type(series) is np.ndarray:
        return series
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


def compare(SAMPLE, USERS, n, database, matrix):
    start = time.time()
    warnings.filterwarnings("ignore", category=SettingWithCopyWarning)
    # SAMPLE = 7500
    # USERS = '../user/simple_users.pkl'
    # database = pd.read_csv('../vectorise_database/gen_normed_np-database.csv', usecols=["tconst", "genres"])
    # matrix = pd.read_csv('../new_matrix.csv')
    # sample = list(database.tconst.values)[0:SAMPLE]  # list of movie ids

    count = 0
    users = []
    all_users = []
    empty = 0

    file = open(USERS, mode="rb")
    while 1:
        try:
            user = pickle.load(file)
            all_users.append(user)
        except EOFError:
            break
    file.close()
    users = random.sample(all_users, k=n)

    # fit = []
    better_avg = {"win": 0, "total": 0}
    better_max = {"win": 0, "total": 0}
    better_sim = {"win": 0, "total": 0}
    sample = database.head(SAMPLE)
    for user in users:
        # comparing with random recommender
        # movie = random.choice(sample)
        # movie = database.head(SAMPLE).sample(n=1)
        movie = sample.head(SAMPLE).sample(n=1)
        # print(movie)

        my_recommended = recommenders.my_recommender(user, movie, database, matrix)
        stat_recommended = recommenders.stat_recommender(all_users, movie, database)
        if stat_recommended.empty:
            empty += 1
            continue
        # print(my_recommended, random_recommended)

        # print(my_recommended)
        my_recommended.loc[:, "genres"] = my_recommended.genres.apply(func=convert_to_numpy)
        stat_recommended.loc[:, "genres"] = stat_recommended.genres.apply(func=convert_to_numpy)
        movie.loc[:, "genres"] = movie.genres.apply(func=convert_to_numpy)

        # print(my_recommended)
        my_recommended = recommenders.add_eval_columns(user, movie, my_recommended)
        stat_recommended = recommenders.add_eval_columns(user, movie, stat_recommended)
        # print(stat_recommended)

        # print(my_recommended["sim"])
        # print(random_recommended["sim"])

        # if my_recommended["avg"].mean() > random_recommended["avg"].mean():
        #     better_avg["win"] += 1
        #
        # if my_recommended["avg"].max() > random_recommended["avg"].max():
        #     better_max["win"] += 1
        #
        # if my_recommended["sim"].mean() > random_recommended["sim"].mean():
        #     better_sim["win"] += 1
        #
        # better_avg["total"] += 1
        # better_max["total"] += 1
        # better_sim["total"] += 1

    # print(better_avg["win"] / better_avg["total"])
    # print("p for avg: ", stats.binom_test(better_avg["win"], better_avg["total"], p=0.5))
    # print(better_max["win"] / better_max["total"])
    # print("p for max: ", stats.binom_test(better_max["win"], better_max["total"], p=0.5))
    # print(better_sim["win"] / better_sim["total"])
    # print("p for sim: ", stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
    print("no stat recommendations in ", empty, " cases")
    print("duration ", time.time() - start, " seconds")

    # analysis output

    # print(better_avg["win"] / better_avg["total"], end=" ")
    # print(stats.binom_test(better_avg["win"], better_avg["total"], p=0.5), end=" ")
    # print(better_max["win"] / better_max["total"], end=" ")
    # print(stats.binom_test(better_max["win"], better_max["total"], p=0.5), end=" ")
    # print(better_sim["win"] / better_sim["total"], end=" ")
    # print(stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
