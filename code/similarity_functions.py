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
from math import isnan
import numpy as np
import numpy.linalg as LA

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


# TODO add support for actors
# TODO Maybe result of a vector would be be more useful then a simple ratio
# FIXME the following lines may have better solutions:
# FIXME 1.)    movie = [item for item in movie if "nm" in item]
# FIXME 1.)    temp = set(our_movie).intersection(movie)d


def people_involved(movie, our_movie):
    # these comments serve to debug code, uncomment them when needed
    # print("ULAZIM")
    # print("Movie : " + str(movie))
    # print("Tip move " + str(type(movie)))
    # print("Series " + str(our_movie))
    # print("Tip series " + str(type(our_movie)))

    movie = str(movie).strip().split()
    our_movie = str(our_movie).strip().split()

    movie = [item for item in movie if "nm" in item]
    our_movie = [item for item in our_movie if "nm" in item]
    temp = set(our_movie).intersection(movie)

    # odkomentirati za debug
    # print("FILTRIRAO")
    # print("Movie : " + str(movie))
    # print("Tip move " + str(type(movie)))
    # print("Series " + str(our_movie))
    # print("Tip series " + str(type(our_movie)))
    # print("Temp : " + str(temp))

    # error handling
    if len(movie) + len(our_movie) - len(temp) == 0:
        return 0
    # true result
    # number of shared elements / number of total elements
    return 1 - float(len(temp) / (len(movie) + len(our_movie) - len(temp)))


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
    temp = set(our_movie).intersection(movie)

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
    return 1 - float(len(temp) / (len(movie) + len(our_movie) - len(temp)))


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
        return 0

    BEGINNING_OF_MOVIE_TIME = 1877
    movie = int(movie) - BEGINNING_OF_MOVIE_TIME
    our_movie = str(our_movie).strip().split()
    our_movie = float(our_movie[1])
    our_movie = our_movie - BEGINNING_OF_MOVIE_TIME

    # NaN handling
    if isnan(our_movie):
        return 0

    # a if condition else b , ternary operator in python
    return 1 - (our_movie / movie) if (our_movie < movie) else 1 - (movie / our_movie)


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


# TODO See if this will be actually used

def remove_least_similar(movies, series):
    return movies


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

    # NaN handling
    if isnan(movie):
        return movie

    movie = float(movie)
    our_movie = str(our_movie).strip().split()
    our_movie = float(our_movie[1])

    # NaN handling
    if isnan(our_movie):
        return our_movie

    # a if condition else b , ternary operator in python
    return 1 - (our_movie / movie) if (our_movie < movie) else 1 - (movie / our_movie)


"""
#
# total_similarity(series)
#
# parameter series is the row upon which function is called
#
# returns Euclidean distance from our movie which is defined as the origin at 0
#
#
"""


def total_similarity(series):
    vector = np.array([series.genres,
                       series.runtimeMinutes,
                       series.directors,
                       series.writers,
                       series.startYear])

    vector = vector[~np.isnan(vector)]
    zeros = np.zeros([len(vector)])

    # for debugg
    # print(zeroes)
    # print(vector)
    result = LA.norm(zeros - vector)
    if isnan(result):
        print(series.primaryTitle)
        print(vector)
        print("-------------------")
    return result


# movies.apply(func=similar.total_similarity,axis=1, args={})
def print_series(series):
    print(series)
    return
