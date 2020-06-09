import pandas as pd
import time
from code import similarity_functions as similar

"""@film is string of our film name,
    later to be refractored to id
    @database is the pandas dataframe containing all movies
    how_many is how many similar films we are searching for
"""


def find_most_similar(film_id, database, how_many):
    start_time = time.time()

    # TODO Optimize all of this one day

    INPUT = str(film_id)
    MOST_SIMILAR = how_many

    # print("Our movie is : " + INPUT)

    # movies = pd.read_csv(str(database))
    input_movie = database.loc[database["tconst"] == INPUT]
    movies = database.loc[database["tconst"] != INPUT]  # remove our selected movie from dataframe

    # -----------filter by isAdult----------------------
    is_adult_start = time.time()
    movies = similar.is_adult_value(movies, input_movie)
    is_adult_end = time.time()

    # ----------izracunaj slicnost direktora-------------
    director_start = time.time()
    movies["directors"] = movies.directors.apply(func=similar.people_involved, args={str(input_movie.directors)})
    director_end = time.time()

    # ------------izracunaj slicnost genre----------
    genre_start = time.time()
    movies["genres"] = movies.genres.apply(func=similar.genres, args={str(input_movie.genres)})
    genre_end = time.time()

    # ----------------slicnost godine-----------------
    year_start = time.time()
    movies["startYear"] = movies.startYear.apply(func=similar.start_year, args={str(input_movie.startYear)})
    year_end = time.time()

    # ----------izracunaj slicnost pisaca------------------
    writer_start = time.time()
    movies["writers"] = movies.writers.apply(func=similar.people_involved, args={str(input_movie.writers)})
    writer_end = time.time()

    # ----------------------------------------------------
    # izbaci one za koji do sada imaju najmanju slicnost
    filter_start = time.time()
    movies = similar.remove_least_similar(movies, input_movie)
    filter_end = time.time()

    # -------------slicnost trajanja------------------
    runtime_start = time.time()
    movies["runtimeMinutes"] = movies.runtimeMinutes.apply(func=similar.runtime, args={str(input_movie.runtimeMinutes)})
    runtime_end = time.time()

    # ----------izracunaj slicnost glumaca-------------
    actors_start = time.time()
    movies["actors"] = movies.actors.apply(func=similar.people_involved, args={str(input_movie.actors)})
    actors_end = time.time()

    # ------------izracunaj zavrsnu slicnost---------------
    total_start = time.time()

    movies["similarity"] = movies.apply(func=similar.total_similarity, axis=1, args={})

    total_end = time.time()
    math_end = time.time()

    # -------------prikazi podatke----------------
    movies = movies.sort_values(by=["similarity"])
    # movies = movies.sort_values(by=["numVotes"], ascending=False)
    movies = movies.head(MOST_SIMILAR)
    movies["movies"] = movies["tconst"]
    movies["tconst"] = INPUT
    movies = movies[["tconst", "similarity", "movies"]]
    return movies
    # movies = movies[["tconst", "similarity", "primaryTitle"]]
    # print(movies["primaryTitle"])
    # print(movies.shape)

    # """all_movies = pd.read_csv("final.csv")
    # # spajanje najslicnijih i svih filmova
    # merged = pd.merge(movies, all_movies, how="inner", on="tconst")
    # del movies
    # del all_movies
    # # merged.apply(func=similar.print_series, axis=1, args={})
    # print(merged[["primaryTitle", "similarity", "averageRating"]])"""

    # print("adult %s" % (is_adult_end - is_adult_start))
    # print("directors %s" % (director_end - director_start))
    # print("writers %s" % (writer_end - writer_start))
    # print("genres %s" % (genre_end - genre_start))
    # print("year %s" % (year_end - year_start))
    # print("--filtering movies %s " % (filter_end - filter_start))
    # print("runtime %s" % (runtime_end - runtime_start))
    # print("actors %s" % (actors_end - actors_start))
    # print("sveukupna slicnost %s" % (total_end - total_start))
    # print("racunanje %s" % (math_end - start_time))
    # print("---program %s seconds ---" % (time.time() - start_time))

# database = pd.read_csv("database.csv")
# find_most_similar("Inception", database, 40)
