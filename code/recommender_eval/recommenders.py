import pandas as pd
import numpy as np

# pseudo of each function
# def x_recommender(user, movie, database, matrix)
# extract recommendations with movie, database and matrix
# for each recommendation get numeric value how good the recco is
# return avg value or something

MAX_NUM_GENRES = 3


def random_recommender(user, movie, database, matrix):
    recommended = database.sample(n=10)
    return recommended


# columns left are similarity, tconst, genres
def my_recommender(user, movie, database, matrix):
    recommended = matrix.loc[matrix["tconst"] == str(movie.tconst.values[0])].head(10)
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
        # result = np.average(result[result != 0]) / (MAX_NUM_GENRES)
        result = np.average(result[result != 0]) / len(result[result != 0])
        return result

    # closer to 1 is better
    def genre_similarity(series):
        genres = movie.genres.values[0]
        result = np.multiply(series, genres)
        return len(result[result != 0]) / len(genres[genres != 0])

    bias = user.get_genre_bias()
    recommended["avg"] = recommended.genres.apply(func=elementwise_avg, args={})
    recommended["sim"] = recommended.genres.apply(func=genre_similarity, args={})

    return recommended
