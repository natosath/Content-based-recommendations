import pandas as pd


# movies["similarity"] = movies.apply(func=similar.total_similarity, axis=1, args={})

def tconst_shorten(series):
    return series.tconst[2:]


movies = pd.read_csv('database.csv')
links = pd.read_csv('links.csv')
links = links.rename(columns={'imdbId': 'tconst'})
# drop rating column
movies["tconst"] = movies.apply(func=tconst_shorten, axis=1, args={})

# print(movies)
# print(links)

# movies = movies.join(other=links, how='inner', on='tconst')
movies = pd.concat([movies, links], axis=1, join='inner', join_axes='tconst')
print(movies)
print(movies.shape)
