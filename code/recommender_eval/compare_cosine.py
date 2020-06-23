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

PATH_COSINE = 'cosine_results.txt'


def jaccard(first, second):
    inter = set(first).intersection(second)
    return len(inter) / (len(set(first).union(second)))


def convert_to_numpy(series):
    if type(series) is np.ndarray:
        return series
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


def compare(SAMPLE, USERS, n, database, e_matrix, c_matrix):
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

    file = open(PATH_COSINE, mode="a")
    # fit = []
    equal = []
    sample = database.head(SAMPLE)
    eu_values = []
    cos_values = []
    for user in users:
        diff = None
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

        euclid = recommenders.add_eval_columns(user, movie, euclid)
        cosine = recommenders.add_eval_columns(user, movie, cosine)

        # euclid = euclid.sort_values(by="rating", ascending=False)
        # cosine = cosine.sort_values(by="rating", ascending=False)
        x = np.array(list(euclid.rating.values))
        y = np.array(list(cosine.rating.values))
        eu_values.extend(list(euclid.rating.values))
        cos_values.extend(list(cosine.rating.values))

        # sim = jaccard(list(euclid.tconst.values),
        #               list(cosine.tconst.values))
        # print(sim)

        # write is tuple of p, w_p, equal

        stat, p = stats.ttest_rel(x, y)
        if math.isnan(p):
            p = 1
        if not np.array_equal(x, y):
            # print(x, y)
            # print(p)
            # print("-----")
            wilcoxon, w_p = stats.wilcoxon(x, y, alternative="greater")
            # print(w_p, statistics.mean(x) >= statistics.mean(y))
            file.write(str(p) + " " + str(w_p) + " " + "0" + "\n")
            continue

        # write is tuple of p, w_p, equal
        # 1 if equal
        file.write(str(p) + " " + "1" + " " + "1" + "\n")

        # print(euclid.rating)
        # print(cosine.rating)
        # print("----")

    # analysis output and file write here
    file.close()
    print(stats.ttest_rel(eu_values, cos_values))
    print(time.time() - start, " seconds")

# better_avg = {"euclid": 0, "cosine": 0, "draw": 0}
# better_max = {"euclid": 0, "cosine": 0, "draw": 0}
# better_sim = {"euclid": 0, "cosine": 0, "draw": 0}


# if euclid["avg"].mean() == cosine["avg"].mean():
#     better_avg["draw"] += 1
# elif euclid["avg"].mean() > cosine["avg"].mean():
#     better_avg["euclid"] += 1
# else:
#     better_avg["cosine"] += 1
#
# if euclid["avg"].max() == cosine["avg"].max():
#     better_max["draw"] += 1
# elif euclid["avg"].max() > cosine["avg"].max():
#     better_max["euclid"] += 1
# else:
#     better_max["cosine"] += 1
#
# if euclid["sim"].mean() == cosine["sim"].mean():
#     better_sim["draw"] += 1
# elif euclid["sim"].mean() > cosine["sim"].mean():
#     better_sim["euclid"] += 1
# else:
#     better_sim["cosine"] += 1

# print(better_avg["euclid"], better_avg["cosine"], better_avg["draw"])
# print(better_max["euclid"], better_max["cosine"], better_max["draw"])
# print(better_sim["euclid"], better_sim["cosine"], better_sim["draw"])


# print(better_avg["win"] / better_avg["total"], end=" ")
# print(stats.binom_test(better_avg["win"], better_avg["total"], p=0.5), end=" ")
# print(better_max["win"] / better_max["total"], end=" ")
# print(stats.binom_test(better_max["win"], better_max["total"], p=0.5), end=" ")
# print(better_sim["win"] / better_sim["total"], end=" ")
# print(stats.binom_test(better_sim["win"], better_sim["total"], p=0.5))
