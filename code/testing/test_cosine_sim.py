import pandas as pd
import numpy as np
from code.testing.cosine_similarity import find_most_similar

# interstellar, godfather, inception, fight club
# films = ["tt0816692", "tt0068646", "tt1375666", "tt0137523"]
database = pd.read_csv('../database.csv')
films = np.array_split(database["tconst"], 3)[0]
for film in films.head(20):
    print(film, " start")
    sims = find_most_similar(film, database, 20)
    # print(sims[["primaryTitle", "similarity"]])
    # print(film, " done, shape: ", sims.shape)
