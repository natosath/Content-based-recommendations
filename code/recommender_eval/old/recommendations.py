import pandas as pd
import numpy as np


def get_genre_bias_from_user(user_data):
    genres = dict()
    for genre, values in user_data.genres.items():
        genres[str(genre)] = values[0] / values[1]
    return genres


def get_recommendations(matrix, movie):
    # matrix = matrix.sort_values(by="similarity")
    return matrix.loc[matrix["movie"] == movie.tconst].head(10)


def analyze_genres(series, df, user_data):
    genres_columns = df["genres"]
    count_all = 0
    score_all = 0
    for genre in genres_columns:
        genre = str(genre).lower().strip().split(",")
        count = len(genre)
        score = 0
        for gen in genre:
            if gen not in user_data.keys():
                count += 1
                continue
            score += user_data[gen]
        score /= count
        score_all += score
        count_all += 1
    if count_all == 0:
        return 0
    return score_all / count_all


def get_winner(series, random, similar, user_data):
    user_data = get_genre_bias_from_user(user_data)
    r = analyze_genres(series, random, user_data)
    s = analyze_genres(series, similar, user_data)
    if s > r:
        return 0
    return 1
