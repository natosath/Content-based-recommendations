import pandas as pd
import random as random

# -------TRENUTNO TESTIRANJE IZVODENJA FUNKCIJA NAD DATAFRAMEMOM------------------

# ovdje napraviti input
INPUT = "Inception"

# trazenje filma po inputu
movies = pd.read_csv("final.csv")
series = movies.loc[(movies["primaryTitle"] == INPUT) or (movies["originalTitle"] == INPUT)]  # ne radi
movies = movies.loc[movies["primaryTitle"] != INPUT]  # bacanje odabranog filma van
movies = movies.drop(labels="primaryTitle", axis=1)

print(series.shape)
print(movies.shape)


def randomNum():
    return random.random()


movies["averageRating"] = randomNum() * movies["averageRating"]

print(movies["averageRating"])
