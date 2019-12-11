import pandas as pd
import time

start_time = time.time()

from code import similarity_functions as similar

# TODO Optimize all of this one day

# TODO Input from keyboard or some other source

INPUT = "The Prestige"
MOST_SIMILAR = 12
# INPUT = str(input("Unesi film"))

print("Our movie is : " + INPUT)

# search our selected movie in dataframe
# movies = pd.read_csv("final.csv")
movies = pd.read_csv("database.csv")
input_movie = movies.loc[movies["primaryTitle"] == INPUT]
movies = movies.loc[movies["primaryTitle"] != INPUT]  # remove our selected movie from dataframe
# movies = movies.drop(labels="originalTitle", axis=1)   # remove to reduce clutter, however it is needed for final out put
print("All movies")
print(movies[["primaryTitle", "averageRating", "genres"]])
print("Our movie")
print(input_movie[["primaryTitle", "averageRating", "genres"]])

"""print(movies, movies.shape)
print(series, series.shape, series.dtypes)"""

# -----------filter by isAdult----------------------

print("isAdult")
movies = similar.is_adult_value(movies, input_movie)
print(movies.shape, movies.dtypes)

# ----------izracunaj slicnost direktora-------------
print("directors")

# u stupac "directors" dataframea movies transformiramo funkcijom calcDirectros, prvi argument pandas interno salje
# drugi argument funkcije calcDirectros salje sa args={}
# ovo ne dirati, radi kako spada
movies["directors"] = movies.directors.apply(func=similar.people_involved, args={str(input_movie.directors)})
print(movies[["primaryTitle", "directors"]])

# ----------izracunaj slicnost pisaca------------------
print("writers")

movies["writers"] = movies.writers.apply(func=similar.people_involved, args={str(input_movie.writers)})
print(movies[["primaryTitle", "writers"]])

# ------------izracunaj slicnost genre----------
print("genres")
# TODO changed here
movies["genres"] = movies.genres.apply(func=similar.genres, args={str(input_movie.genres)})
print(movies[["primaryTitle", "genres"]])

# -----za version 2.0 izracunaj slicnost glumacke postave
#
# ovdje ce ici nesto tipa movies["actors"] = movies.actors.apply(func=sim.list_like, args={str(series.actors)})
#
# ----------------------------------------------#:

# izbaci one za koji slicnost(direktor) i slicnost(genre) je 0
print("first removal pass")
movies = similar.remove_least_similar(movies, input_movie)

# izracunaj slicnost startYear
print("startYear")

# print(movies[["primaryTitle", "startYear"]])
print(input_movie.startYear)
movies["startYear"] = movies.startYear.apply(func=similar.start_year, args={str(input_movie.startYear)})
print(movies[["primaryTitle", "startYear"]])

# izracunaj slicnost runtimeMinutes
print("startYear")

print(movies[["primaryTitle", "runtimeMinutes"]])
print(input_movie.startYear)
movies["runtimeMinutes"] = movies.runtimeMinutes.apply(func=similar.runtime, args={str(input_movie.runtimeMinutes)})
print(movies[["primaryTitle", "startYear"]])

# ----------izracunaj slicnost glumaca-------------
print("actors")

# u stupac "directors" dataframea movies transformiramo funkcijom calcDirectros, prvi argument pandas interno salje
# drugi argument funkcije calcDirectros salje sa args={}
# ovo ne dirati, radi kako spada
movies["actors"] = movies.actors.apply(func=similar.people_involved, args={str(input_movie.actors)})
print(movies[["primaryTitle", "actors"]])

# # izracunaj slicnost rating
# print("rating")
#
# print(movies[["primaryTitle", "averageRating"]])
# print(input_movie.startYear)
# movies["averageRating"] = movies.averageRating.apply(func=similar.rating, args={str(input_movie.averageRating)})
# print(movies[["primaryTitle", "averageRating"]])

# # izracunaj slicnost numVotes
# print("num of votes")
#
# print(movies[["primaryTitle", "numVotes"]])
# print(input_movie.startYear)
# movies["numVotes"] = movies.numVotes.apply(func=similar.rating, args={str(input_movie.averageRating)})
# print(movies[["primaryTitle", "numVotes"]])

# izracunaj zavrsnu slicnost
print("zavrsna slicnost")

movies["similarity"] = movies.apply(func=similar.total_similarity, axis=1, args={})
movies = movies.sort_values(by=["similarity"])
# micanje nepotrebnih stvari
movies = movies[["tconst", "similarity"]]
# uzimanje najslicnijih
movies = movies.head(MOST_SIMILAR)

all_movies = pd.read_csv("final.csv")
# spajanje najslicnijih i svih filmova
merged = pd.merge(movies, all_movies, how="inner", on="tconst")
del movies
del all_movies
# merged.apply(func=similar.print_series, axis=1, args={})
print(merged[["primaryTitle", "similarity", "averageRating"]])

print("--- %s seconds ---" % (time.time() - start_time))
