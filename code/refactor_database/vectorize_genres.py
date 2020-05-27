import pandas as pd
import numpy as np

path = '../database.csv'
database = pd.read_csv(path)
database.info(verbose=True)
genres = pd.unique(database["genres"]).tolist()
# genres = list(map(str.lower, genres))
genres_dict = {}
genres = [genre for genre in genres if type(genre) is str]  # remove nan
genres = [genre.lower() for genre in genres]  # lowercase it
genres = sorted(genres)
count = 0
for genre in genres:
    for gen in genre.strip().split(","):
        if gen not in genres_dict.keys():
            genres_dict[gen] = count
            count += 1


# print(genres_dict)


# print(genres)

# for i in range(len(genres)):
#     genres_dict[genres[i]] = i


# print(genres_dict)


def vectorize_genres(series):
    gens = series.genres
    vector = [0] * len(genres_dict.keys())
    if type(gens) != str:  # nan handling
        return vector
    for gen in gens.lower().strip().split(","):
        # if gen not in genres_dict.keys():
        #     genres_dict[gen] = len(genres_dict.keys())
        #     vector.append(0)
        index = genres_dict[gen]
        vector[index] = 1
    vector = np.array(vector)
    if len(vector) != 26:
        print(len(vector), vector)
    return [vector]  # wrap np array for storage


database["genres"] = database.apply(func=vectorize_genres, axis=1, args={})
database.info(verbose=True)
# print(database.head(1)["primaryTitle"])
# print(database[["genres"]])
# print(genres_dict)

# genres = [genre for genre in genres if not "," in genre]
# print(genres)

# actors = database.iloc[3]["actors"].strip().split(",")
# for actor in actors:
#     print(actor[2:])
# actors = [int(actor[2:]) for actor in actors]
# print(actors)
