import pandas as pd
import collections

genres = dict()
combos = dict()


# TODO make another for each genre pair


def to_lower(series):
    return str(series.genres).lower()


def analyze_genres(series):
    global genres, combos
    if series.genres not in combos.keys():
        combos[series.genres] = 0
    combos[series.genres] += 1
    allgens = series.genres.strip().split(",")
    for gen in allgens:
        if gen not in genres.keys():
            genres[gen] = 0
        genres[gen] += 1


def count_genres(series):
    gens = series.genres.strip().split(",")
    return len(gens)


path = '/home/natosath/Desktop/Projekt/code/new_database.csv'
database = pd.read_csv(path, usecols=['genres', 'primaryTitle'])
database = database.head(7500)
database['genres'] = database.apply(func=to_lower, axis=1, args={})
database['num'] = database.apply(func=count_genres, axis=1, args={})
database.apply(func=analyze_genres, axis=1, args={})
# print(database)
genres = collections.OrderedDict(genres)
combos = collections.OrderedDict(combos)

with open('genre_data.txt', mode="w") as file:
    for key, value in sorted(genres.items(), key=lambda item: item[1], reverse=True):
        print(key, value)
        # žanr num_pojava udio_u_%
        file.write(str(key) + " " + str(value) + " " + str(value / 7500 * 100) + "\n")
print("------------")
for key, value in combos.items():
    if value < 5:
        print(key, value)

for i in range(1, 3 + 1):
    num = database.loc[database["num"] == i]
    print(len(num.index))
