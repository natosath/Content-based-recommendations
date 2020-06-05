import pandas as pd

columns = ["tconst", "movie", "similarity"]
matrix = pd.read_csv('../matrix.csv', usecols=columns)
cosine = pd.read_csv('cosine_matrix.csv', usecols=columns)

merged = cosine.merge(matrix, on="movie", how="inner")
print(merged)
