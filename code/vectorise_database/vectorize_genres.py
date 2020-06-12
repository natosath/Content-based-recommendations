import pandas as pd
import numpy as np
import pickle
import time

start = time.time()
path = '../new_database.csv'
database = pd.read_csv(path)
database = database.drop(columns=["Unnamed: 0"], axis=1)
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
    # vector = np.array(vector)
    # if len(vector) != 26:
    #     print(len(vector), vector)
    return vector


database["genres"] = database.apply(func=vectorize_genres, axis=1, args={})

database.to_csv('gen_normed_np-database.csv', index=False)
database.to_pickle('gen_normed_np-database.zip', protocol=pickle.HIGHEST_PROTOCOL)
database.info(verbose=True)

with open('genres.txt', mode='w') as file:
    for key, value in genres_dict.items():
        file.write(str(value + 1) + " - > " + str(key + "\n"))
with open('genres.pkl', mode='wb') as file:
    pickle.dump(genres_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

print(time.time() - start, " seconds")

# def vectorize_genres(series):
#     gens = series.genres
#     vector = [0] * len(genres_dict.keys())
#     if type(gens) != str:  # nan handling
#         return vector
#     for gen in gens.lower().strip().split(","):
#         # if gen not in genres_dict.keys():
#         #     genres_dict[gen] = len(genres_dict.keys())
#         #     vector.append(0)
#         index = genres_dict[gen]
#         vector[index] = 1
#     vector = np.array(vector)
#     if len(vector) != 26:
#         print(len(vector), vector)
#     return [vector]  # wrap np array for storage
