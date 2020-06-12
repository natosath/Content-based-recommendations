# actors_by_film = actor.groupby("tconst").nconst.sum()
import pandas as pd


def get_movies(series):
    global matrix
    filtered = matrix.loc[matrix.tconst == series.tconst]
    movies = list(filtered["movie"].values)
    return movies


def adjust_movies(series):
    movies = series.strip().split("tt")
    output = ""
    for movie in movies:
        output += "tt" + movie + ","
    print(output[0:-1])
    return series


matrix = pd.read_csv('../new_matrix.csv')
df = pd.DataFrame()
# matrix.apply(func=get_movies, axis=1)
df["tconst"] = matrix["tconst"].unique()
df["movies"] = df.apply(func=get_movies, axis=1)
df.to_csv('similars_in_list.csv')

# matrix["movie"] = matrix.movie.apply(func=adjust_movies, args={})
# print(len(matrix["movie"].unique()))
# matrix.info(verbose=True)
# print(matrix["movie"])
