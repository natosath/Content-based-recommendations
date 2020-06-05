"""
#
# This file contains functions that will be used to calculate similarity between our movie of choice
# and the movies contained within the dataframe "movie"
#
"""

# TODO Add actor support to people_involved
# TODO Add function which calc similarity for runtime
# TODO NaN Error handling
# TODO Add function which uses averageRating and numVotes
# TODO Function which uses all the value calculated and returns final similarity

import pandas as pd
from math import isnan, acos, pi
from math import log10
import numpy as np
import numpy.linalg as LA

ones = {5: np.ones(5), 6: np.ones(6)}

"""
# 
# is_adult_value(movies, our_movie)
#
# parameter "movie" represents the Dataframe which contains the info for all movies
# parameter "our_movie" represent the Series which contains the info of our selected movie
#
# returns Dataframe which contains the same "isAdult" value as our_movie
#
# note : isAdult means pornographic, not rated for mature audiences
# the rationale behind this is that someone looking at pornographic content would prefer other pornographic content
  and vice-versa, someone looking at "standard" movies would prefer non-pornographic content
#
"""


def is_adult_value(movie, our_movie):
    isAdult = int(our_movie["isAdult"])
    movie = movie.loc[movie["isAdult"] == isAdult]
    movie = movie.drop("isAdult", axis=1)  # ne treba vise za izracun
    return movie


"""
#
# people_involved(movie, our_movie):
#
# parameter "movie" represents the data from the movie being compared to our movie
# parameter "our_movie" represents the data from our movie
#
# Returns value from 0 to 1 which represents the Jaccard distance
  1 - (num of shared people of certain category) / (num of people between movie and our_movie)
#
# can be used on writers, directors for now
#
"""


# faster version, have to check if it is equally as accurate
def people_involved(movie, our_movie):
    movie = str(movie).strip().split()
    our_movie = str(our_movie).strip().split()

    # people's ID begin with "nm"
    movie = {item for item in movie if "nm" in item}
    our_movie = {item for item in our_movie if "nm" in item}
    temp = movie & our_movie
    # error handling
    if len(movie) + len(our_movie) - len(temp) == 0:
        return 0
    # true result
    # number of shared elements / number of total elements
    return float(len(temp) / (len(movie) + len(our_movie) - len(temp)))


"""
#
# genres(movie, our_movie):
#
# parameter "movie" represents the data from the movie being compared to our movie
# parameter "our_movie" represents the data from our movie
#
# Returns value from 0 to 1 which represents the Jaccard distance
# (num of shared genres) / (num of genres between movie and our_movie)
# 
#
"""


def genres(movie, our_movie):
    # these comments serve to debug code, uncomment them when needed
    # print("ULAZIM u genres")
    # print("Movie : " + str(movie))
    # print("Tip move " + str(type(movie)))
    # print("Series " + str(our_movie))
    # print("Tip series " + str(type(our_movie)))

    movie = str(movie).strip().split()
    our_movie = str(our_movie).strip().split()
    temp = set(movie).intersection(our_movie)

    # print("FILTRIRAO u genres")
    # print("Movie : " + str(movie))
    # print("Tip move " + str(type(movie)))
    # print("Series " + str(our_movie))
    # print("Tip series " + str(type(our_movie)))
    # print("Intersection : " + str(temp))

    # error handling
    if len(movie) + len(our_movie) - len(temp) == 0:
        return 0
    # true result
    # number of shared elements / number of total elements
    return float(len(temp) / (len(movie) + len(our_movie) - len(temp)))


# def genres(movie, our_movie):
#     # these comments serve to debug code, uncomment them when needed
#     # print("ULAZIM u genres")
#     # print("Movie : " + str(movie))
#     # print("Tip move " + str(type(movie)))
#     # print("Series " + str(our_movie))
#     # print("Tip series " + str(type(our_movie)))
#
#     movie = set(str(movie).strip().split())
#     our_movie = set(str(our_movie).strip().split())
#     temp = our_movie & movie
#
#     # print("FILTRIRAO u genres")
#     # print("Movie : " + str(movie))
#     # print("Tip move " + str(type(movie)))
#     # print("Series " + str(our_movie))
#     # print("Tip series " + str(type(our_movie)))
#     # print("Intersection : " + str(temp))
#
#     # error handling
#     if len(movie) + len(our_movie) - len(temp) == 0:
#         return 0
#     # true result
#     # number of shared elements / number of total elements
#     return 1 - float(len(temp) / (len(movie) + len(our_movie) - len(temp)))


"""
#
# start_year(movie, our_movie)
#
# parameter "movie" represents the data from the movie being compared to our movie
# parameter "our_movie" represents the data from our movie
# constant BEGINNING_OF_MOVIE_TIME is the year film began subtracted by 1
#
# Returns value from 0 to 1 which represents the difference between start years
#
# normalises startYear by subtracting BEGINNING_OF_MOVIE_TIME to make better spread from 0 to 1
# if startYear were not normalised all values would be from ~0.93 to 1
# as movies are a relatively new art form they can wary greatly by decade in style, language used, production quality,
  special effects, actors ect
# 
#
"""


def start_year(movie, our_movie):
    # trebam 1 - pomak, ako su iste godine rezultat treba biti 1, sto su dalji to je blize nuli

    # uncomment for debugg
    # print("ULAZIM u start_year")
    # print("Movie : " + str(movie))
    # print("Series " + str(our_movie))
    # print("Tip series " + str(type(our_movie)))

    # NaN handling
    if isnan(movie):
        return 1

    BEGINNING_OF_MOVIE_TIME = 1877
    movie = int(movie) - BEGINNING_OF_MOVIE_TIME
    our_movie = str(our_movie).strip().split()
    our_movie = float(our_movie[1])
    our_movie = our_movie - BEGINNING_OF_MOVIE_TIME

    # NaN handling
    if isnan(our_movie):
        return 1

    # a if condition else b , ternary operator in python
    return (our_movie / movie) if (our_movie < movie) else (movie / our_movie)


"""
#
# remove_least_similar(movies, series):
#
# parameter "movie" represents the Dataframe which contains the info for all movies
# parameter "our_movie" represent the Series which contains the info of our selected movie
#
# removes movies whose similarity will be low in order to optimize process
# the movies are chosen based on their directors, writers and later actors value
#
"""


# TODO Optimize this
# Primary criteria for now:
# genre, director, startYear
# kada pretvoris ID-jeve osoba u intove, pokusaj opet sve racunati i onda prije
# zavrsne udaljenosti isfiltriraj
def remove_least_similar(movies, series):
    print(movies.shape)
    movies = movies.loc[movies["genres"] != 0]
    print(movies.shape)
    movies = movies.loc[((movies["genres"] != 0) | (movies["directors"] != 0) | (movies["writers"] != 0))
                        & (movies["startYear"] > 0.5)]
    print(movies.shape)

    return movies


# def is_adult_value(movie, our_movie):
#     isAdult = int(our_movie["isAdult"])
#     movie = movie.loc[movie["isAdult"] == isAdult]
#     movie = movie.drop("isAdult", axis=1)  # ne treba vise za izracun
#     return movie


"""
#
# runtime(movie, our_movie)
#
# parameter "movie" represents the data from the movie being compared to our movie
# parameter "our_movie" represents the data from our movie
#
# Returns value from 0 to 1 which represents the difference between runtime
#
# Nothing special, just the ratio of runtime
#
"""


def runtime(movie, our_movie):
    # uncomment for debugg
    # print("ULAZIM u start_year")
    # print("Movie : " + str(movie))
    # print("Series " + str(our_movie))

    # NaN handling to avoid calculation of something that will result in NaN
    if isnan(movie):
        return movie

    movie = float(movie)
    our_movie = str(our_movie).strip().split()
    our_movie = float(our_movie[1])

    # NaN handling
    if isnan(our_movie):
        return our_movie

    # a if condition else b , ternary operator in python
    return (our_movie / movie) if (our_movie < movie) else (movie / our_movie)


def cosine_similarity(x, y):
    # v_hat = v / np.linalg.norm(v)
    rez = np.dot(x, y) / (np.linalg.norm(x) * (np.linalg.norm(y)))
    return rez

    # dot = unitA * unitB * cosalpha
    # implements cosine distance


def total_similarity(series):
    vector = np.array([series.genres,
                       series.runtimeMinutes,
                       series.directors,
                       series.writers,
                       series.startYear,
                       series.actors])

    # vector = vector * series.averageRating
    # vector = vector * series.numVotes

    vector = vector[~np.isnan(vector)]

    # for debugg
    # print(zeroes)
    # print(vector)
    return cosine_similarity(ones[len(vector)], vector)


# movies.apply(func=similar.print_series,axis=1, args={})
def print_series(series):
    print(series)
    return
