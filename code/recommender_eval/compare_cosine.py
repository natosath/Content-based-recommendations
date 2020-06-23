# oboje koriste my recommender samo je razlika u matrici
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


def convert_to_numpy(series):
    if type(series) is np.ndarray:
        return series
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


def compare(SAMPLE, USERS, n, database, e_matrix, c_matrix):
    # SAMPLE = 7500
    # USERS = '../user/simple_users.pkl'
    # database = pd.read_csv('../vectorise_database/gen_normed_np-database.csv', usecols=["tconst", "genres"])
    # matrix = pd.read_csv('../new_matrix.csv')
    # sample = list(database.tconst.values)[0:SAMPLE]  # list of movie ids

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
    better_avg = {"euclid": 0, "cosine": 0, "draw": 0}
    better_max = {"euclid": 0, "cosine": 0, "draw": 0}
    better_sim = {"euclid": 0, "cosine": 0, "draw": 0}
    sample = database.head(SAMPLE)
    for user in users:
        # comparing with random recommender

        # movie = sample.head(SAMPLE).sample(n=1)

        movie = random.sample(user.watched, k=1)[0]
        movie = sample.loc[sample["tconst"] == str(movie)]
        # print(movie)
        if movie.empty:
            continue

        euclid = recommenders.my_recommender(user, movie, database, e_matrix)
        cosine = recommenders.my_recommender(user, movie, database, c_matrix)
        # print(euclid, cosine)

        # print(euclid)
        euclid.loc[:, "genres"] = euclid.genres.apply(func=convert_to_numpy)
        cosine.loc[:, "genres"] = cosine.genres.apply(func=convert_to_numpy)
        movie.loc[:, "genres"] = movie.genres.apply(func=convert_to_numpy)

        # print(euclid.genres)
        # print(user.get_genre_bias())
        euclid = recommenders.add_eval_columns(user, movie, euclid)
        # print(euclid.genres)
        cosine = recommenders.add_eval_columns(user, movie, cosine)

        # print(euclid["sim"])
        # print(cosine["sim"])
        # a if condition else b
        # better_avg["euclid"] += 1 if euclid["avg"].mean() > cosine["avg"].mean() else better_avg["cosine"]
        # better_max["euclid"] += 1 if euclid["avg"].max() > cosine["avg"].max() else better_max["cosine"]
        # better_sim["euclid"] += 1 if euclid["sim"].mean() > cosine["sim"].mean() else better_sim["cosine"]

        if euclid["avg"].mean() == cosine["avg"].mean():
            better_avg["draw"] += 1
        elif euclid["avg"].mean() > cosine["avg"].mean():
            better_avg["euclid"] += 1
        else:
            better_avg["cosine"] += 1

        if euclid["avg"].max() == cosine["avg"].max():
            better_max["draw"] += 1
        elif euclid["avg"].max() > cosine["avg"].max():
            better_max["euclid"] += 1
        else:
            better_max["cosine"] += 1

        if euclid["sim"].mean() == cosine["sim"].mean():
            better_sim["draw"] += 1
        elif euclid["sim"].mean() > cosine["sim"].mean():
            better_sim["euclid"] += 1
        else:
            better_sim["cosine"] += 1

        # print(euclid["sim"])
        # print(cosine["sim"])
        # print("-----")

    # analysis output

    print(better_avg["euclid"], better_avg["cosine"], better_avg["draw"])
    print(better_max["euclid"], better_max["cosine"], better_max["draw"])
    print(better_sim["euclid"], better_sim["cosine"], better_sim["draw"])
    # print(better_avg["win"] / better_avg["total"], end=" ")
    # print(stats.binom_test(better_avg["win"], better_avg["total"], p=0.5), end=" ")
    # print(better_max["win"] / better_max["total"], end=" ")
    # print(stats.binom_test(better_max["win"], better_max["total"], p=0.5), end=" ")
    # print(better_sim["win"] / better_sim["total"], end=" ")
    # print(stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
