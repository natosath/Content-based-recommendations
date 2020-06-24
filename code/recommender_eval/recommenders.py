import pandas as pd
import numpy as np
from collections import Counter
import statistics

# pseudo of each function
# def x_recommender(user, movie, database, matrix)
# extract recommendations with movie, database and matrix
# for each recommendation get numeric value how good the recco is
# return avg value or something

MAX_NUM_GENRES = 3
NUM_FILMS = 20


def random_recommender(user, movie, database, matrix):
    recommended = database.sample(n=NUM_FILMS)
    return recommended


def stat_recommender(users, movie, database):
    counter = Counter()
    tconst = str(movie.tconst.values[0])
    filtered = [user for user in users if tconst in user.watched]
    for user in filtered:
        counter.update(user.watched)
    common = counter.most_common(20 + 1)
    common = [x[0] for x in common[1:]]
    recommended = database[database.tconst.isin(common)]
    return recommended


# columns left are similarity, tconst, genres
def my_recommender(user, movie, database, matrix):
    recommended = matrix.loc[matrix["tconst"] == str(movie.tconst.values[0])].head(NUM_FILMS)
    recommended = recommended.drop(columns="tconst")
    recommended = pd.merge(recommended, database,
                           left_on=["movie"],
                           right_on=["tconst"],
                           how="left")
    recommended = recommended.drop(columns="movie")
    return recommended


# add avg, weighted genre and genre sim
def add_eval_columns(user, movie, recommended):
    def elementwise_avg(series):
        result = np.multiply(series, bias)
        if np.count_nonzero(result) == 0:
            return 0
        result = result[result != 0]
        return statistics.mean(result)

    # closer to 1 is better
    def genre_similarity(series):
        genres = movie.genres.values[0]
        result = np.multiply(series, genres)
        return len(result[result != 0]) / len(genres[genres != 0])

    bias = user.get_genre_bias()
    recommended.loc[:, "rating"] = recommended.genres.apply(func=elementwise_avg, args={})
    recommended.loc[:, "sim"] = recommended.genres.apply(func=genre_similarity, args={})

    return recommended
