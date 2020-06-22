import pandas as pd
import numpy as np
import multiprocessing as mp
import pickle
import time

from pandas.core.common import SettingWithCopyWarning

from code.recommender_eval import recommenders
import random
from scipy import stats
import warnings

start = time.time()


# def convert_to_numpy(series):
#     array = str(series[1:-1]).strip().replace(",", "").split(" ")
#     array = [float(x) for x in array]
#     return np.array(array)


def convert_to_numpy(series):
    if type(series) is np.ndarray:
        return series
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    if "[" in array:
        print("HERERE", array)
    # print(array)
    array = [float(x) for x in array]
    # print(array)
    return np.array(array)


def compare(SAMPLE, USERS, n, database, matrix, ):
    warnings.filterwarnings("ignore", category=SettingWithCopyWarning)

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
    popular_recommendation = database.head(20)
    # print(popular_recommendation)
    # popular_recommendation["genres"] = popular_recommendation.genres.apply(func=convert_to_numpy)
    popular_recommendation.loc[:, "genres"] = popular_recommendation.genres.apply(func=convert_to_numpy)

    for user in users:
        # comparing with random recommender
        # movie = random.choice(sample)
        movie = database.head(7500).sample(n=1)
        # print(movie)

        my_recommended = recommenders.my_recommender(user, movie, database, matrix)
        # print(my_recommended, random_recommended)

        # print(my_recommended)
        # convert genre column from str to numpy array
        my_recommended.loc[:, "genres"] = my_recommended.genres.apply(func=convert_to_numpy)
        movie.loc[:, "genres"] = movie.genres.apply(func=convert_to_numpy)

        # print(my_recommended
        my_recommended = recommenders.add_eval_columns(user, movie, my_recommended)
        popular_recommendation = recommenders.add_eval_columns(user, movie, popular_recommendation)

        if my_recommended["avg"].mean() > popular_recommendation["avg"].mean():
            better_avg["win"] += 1

        if my_recommended["avg"].max() > popular_recommendation["avg"].max():
            better_max["win"] += 1

        if my_recommended["sim"].mean() > popular_recommendation["sim"].mean():
            better_sim["win"] += 1

        better_avg["total"] += 1
        better_max["total"] += 1
        better_sim["total"] += 1

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
