from collections import Counter
import pickle
import random
import time
import pandas as pd
import math
import numpy as np
import statistics
import warnings
from pandas.core.common import SettingWithCopyWarning
from code.recommender_eval import recommenders
from code.recommender_eval.compare_popular import convert_to_numpy
from sklearn.metrics import mean_squared_error
import scipy.stats as stats

warnings.filterwarnings("ignore", category=SettingWithCopyWarning)
start = time.time()


def elementwise_avg(series):
    result = np.multiply(series, bias)
    if np.count_nonzero(result) == 0:
        return 0
    result = result[result != 0]

    # rez = None
    # diff = 100
    # values = [statistics.mean(result[result != 0]), max(result[result != 0]), min(result[result != 0])]
    # for value in values:
    #     if abs(value - avg) < diff:
    #         rez = value
    #         diff = abs(value - avg)
    # return rez

    return statistics.mean(result) - 0.1
    # return statistics.mean([avg, max(result)])
    # return statistics.mean([avg, statistics.median(result)])
    # return statistics.mean([avg, np.average(result)])

    # return min(result[result != 0])
    # return statistics.mean(result[result != 0])
    # return max(result[result != 0])

    # result = result[result != 0]
    # return np.average(result + -0.5)


def get_rating(series):
    return user.test[str(series)]


bar = [[1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2, 3, 3, 3], {1, 4, 6}]
counter = Counter()
USERS = '../user/simple_users.pkl'
NEW_USERS = '../user/new_simple_users.pkl'
NEWER_USERS = '../user/newer_simple_users.pkl'
TEST_USERS = '../user/test_simple_users.pkl'
c = 0
n = 500

all_users = []
num_watched = []
ratings = []
avgs = []
file = open(TEST_USERS, mode="rb")
take = True
while 1:
    try:
        user = pickle.load(file)
        # num_watched.append(len(user.watched.keys()))
        # ratings.extend(user.watched.values())
        # avgs.append(statistics.mean(user.watched.values()))

        all_users.append(user)

    except EOFError:
        break
    # c += 1
    if c >= n:
        break
# file = open(USERS, mode="rb")
# while 1:
#     try:
#         user = pickle.load(file)
#         users.append(user)
#         num_watched.append(len(user.watched))
#     except EOFError:
#         break
file.close()
# movies watched : num users, key : value


df = pd.read_csv('../vectorise_database/gen_normed_np-database.csv', usecols=["tconst", "genres"])
df.loc[:, "genres"] = df.genres.apply(func=convert_to_numpy)
# begin for if want to repeat
write = open('new_rating_prediction_data.txt', mode="a")
for i in range(100):
    test = []
    predict = []
    users = random.sample(all_users, k=n)
    for user in users:
        watched = df[df["tconst"].isin(list(user.test.keys()))]
        watched["rating"] = watched.tconst.apply(func=get_rating)
        # watched["genres"] = watched["genres"] * user.get_genre_bias()
        # x.apply(lambda x: x * y)
        bias = user.get_genre_bias()
        avg = statistics.mean(user.train.equals())
        # watched["genres"] = df.genres.apply(lambda x: x * bias)
        watched.loc[:, "avg"] = watched.genres.apply(func=elementwise_avg, args={})
        # print(watched[["rating", "avg"]])
        test.extend(list(watched.rating.equals))
        predict.extend(list(watched.avg.equals))
        # rms = np.sqrt(mean_squared_error(list(watched.rating.values),
        #                                  list(watched.avg.values)))
        # print(rms)
    # print(np.array(test) - np.array(predict))
    rme = mean_squared_error(np.array(test), np.array(predict))
    rmse = np.sqrt(rme)
    t, p = stats.ttest_rel(test, predict)
    # print(rme)
    print(rmse)
    print(stats.ttest_rel(test, predict))
    # print(stats.ranksums(test, predict))
    # print(stats.wilcoxon(test, predict))
    print("filmova odradeno ", len(test))
    print("-----------")
    write.write(str(rmse) + " " + str(p) + " " + str(len(test)) + "\n")
# # bunch of stats
# counter.update(num_watched)
# print("num of users: ", len(users))
# print("min", min(num_watched))
# print("max", max(num_watched))
# print("num of users", sum(counter.values()))
# # koliko korisnika je pogledalo vise od 100 filmova
# print(sum({key: value for key, value in counter.items() if key > 100}.values()))
# # % korisnika kojih je pogledalo vise od 100 filmova
# print(100 * sum({key: value for key, value in counter.items() if key < 67}.values()) / len(num_watched), "%")
# print("median", statistics.median(num_watched))
# print(sorted(counter.keys(), reverse=True))
# # --- rating stats
# print(min(avgs))
# print("mean of ratings individual users make", statistics.mean(avgs))
# print("meadian of ratings individual users make", statistics.median(avgs))
# print("median of ratings", statistics.median(ratings))
# print("average rating of all movies", statistics.mean(ratings))
# print("rating, num of votes")
# ratings = Counter(ratings)
# for pair in ratings.most_common():
#     print(pair)
print(time.time() - start, " seconds")
