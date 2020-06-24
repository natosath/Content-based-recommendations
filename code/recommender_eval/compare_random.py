# oboje koriste my recommender samo je razlika u matrici
import pandas as pd
import numpy as np
import multiprocessing as mp
import pickle
import time
import math
import statistics
from pandas.core.common import SettingWithCopyWarning

from code.recommender_eval import recommenders
import random
from scipy import stats
import warnings

PATH_RANDOM = 'random_results.txt'


def jaccard(first, second):
    inter = set(first).intersection(second)
    return len(inter) / (len(set(first).union(second)))


def convert_to_numpy(series):
    if type(series) is np.ndarray:
        return series
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


def compare(SAMPLE, USERS, n, database, matrix):
    start = time.time()
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

    file = open(PATH_RANDOM, mode="a")
    # fit = []
    equal = []
    sample = database.head(SAMPLE)
    eu_values = []
    cos_values = []
    wins = {"my": 0, "total": 0}
    for user in users:
        win = 0
        # movie = sample.head(SAMPLE).sample(n=1)
        movie = random.sample(user.watched, k=1)[0]
        movie = sample.loc[sample["tconst"] == str(movie)]
        # print(movie)
        if movie.empty:
            continue
        my_system = recommenders.my_recommender(user, movie, database, matrix)
        random_system = recommenders.random_recommender(user, movie, database, matrix)
        # print(my_system, random_system)

        # print(my_system)
        my_system.loc[:, "genres"] = my_system.genres.apply(func=convert_to_numpy)
        random_system.loc[:, "genres"] = random_system.genres.apply(func=convert_to_numpy)
        movie.loc[:, "genres"] = movie.genres.apply(func=convert_to_numpy)

        my_system = recommenders.add_eval_columns(user, movie, my_system)
        random_system = recommenders.add_eval_columns(user, movie, random_system)

        HEAD = min(len(my_system.index), len(random_system.index))

        my_system = my_system.sort_values(by="rating", ascending=False).head(HEAD)
        random_system = random_system.sort_values(by="rating", ascending=False).head(HEAD)

        x = np.array(list(my_system.rating.values))
        y = np.array(list(random_system.rating.values))
        eu_values.extend(list(my_system.rating.values))
        cos_values.extend(list(random_system.rating.values))

        # sim = jaccard(list(my_system.tconst.values),
        #               list(random_system.tconst.values))
        # print(sim)

        stat, p = stats.ttest_rel(x, y)
        if math.isnan(p):
            p = 1
        wilcoxon, w_p_g = stats.wilcoxon(x, y, alternative="greater")
        wilcoxon2, w_p = stats.wilcoxon(x, y)
        # tuple p student, p wilcox, p wilcox greater, equal

        if my_system["rating"].mean() > random_system["rating"].mean():
            win = 1
            wins["my"] += 1
        if my_system["rating"].mean() != random_system["rating"].mean():
            wins["total"] += 1

        file.write(str(p) + " " + str(w_p) + " " + str(w_p_g) + " " + str(win) + "\n")

        # print(my_system.rating)
        # print(random_system.rating)
        # print("----")

    # analysis output and file write here
    file.close()
    print(stats.ttest_rel(eu_values, cos_values))
    print(stats.wilcoxon(eu_values, cos_values))
    print(stats.wilcoxon(eu_values, cos_values, alternative="greater"))
    print(stats.binom_test(wins["my"], wins["total"], p=0.5))
    print("wins", wins["my"] / wins["total"])
    print(time.time() - start, " seconds")
