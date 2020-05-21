import pandas as pd
import time

start = time.time()


def normalize_tconst(series):
    tconst = "tt" + str(series.imdbId)
    return tconst


path_links = '/home/natosath/Desktop/Projekt/movie-lens-csv/links.csv'
path_ratings = '/home/natosath/Desktop/Projekt/movie-lens-csv/ratings.csv'
destination = '/home/natosath/Desktop/Projekt/movie-lens-csv/my_ratings_imdb_id.csv'

links = pd.read_csv(path_links, usecols=["movieId", "imdbId"], dtype={"imdbId": str})
ratings = pd.read_csv(path_ratings, usecols=["userId", "movieId", "rating"], chunksize=300_000)

first = True
for rating in ratings:
    imdb_ratings = links.merge(rating)
    imdb_ratings["tconst"] = imdb_ratings.apply(func=normalize_tconst, axis=1, args={})
    imdb_ratings = imdb_ratings.drop(axis=1, columns=["movieId", "imdbId"])
    print("time elapsed: ", time.time() - start)
    if first:
        imdb_ratings.to_csv(destination, mode="a")
        first = False
    else:
        imdb_ratings.to_csv(destination, mode="a", header=False)

print("done in: ", time.time() - start, " seconds")
