import pandas as pd

# -------TRENUTNO TESTIRANJE LIST-LIKE IN SIM_FUNC------------------

# ovdje napraviti input
INPUT = "Inception"

# trazenje filma po inputu
movies = pd.read_csv("final.csv")
series = movies.loc[movies["primaryTitle"] == INPUT]
movies = movies.loc[movies["primaryTitle"] != INPUT]  # bacanje odabranog filma van


# print(series.columns)


def calcDirectors(movie, series):
    movie = str(movie).strip().split()
    series = str(series).strip().split()

    movie = [item for item in movie if "nm" in item]
    series = [item for item in series if "nm" in item]
    temp = set(series).intersection(movie)

    # odkomentirati za debug
    """print("FILTRIRAO")
    print("Movie : " + str(movie))
    print("Tip move " + str(type(movie)))
    print("Series " + str(series))
    print("Tip series " + str(type(series)))
    print("Temp : " + str(temp))"""

    return len(temp) / (len(movie) + len(series) - len(temp))






def returnZero(nesto, moje):
    print("ulazim u retrun Zero")

    print(nesto)
    print(type(nesto))

    print(moje)
    print(type(moje))

    return 0


#movies["directors"] = calcDirectors(movies, series)
#movies["directors"] = movies.apply(func=calcDirectors(movies, series), axis=0)
#movies = movies.sort_values(by="directors", axis=1, ascending=True)

#movies["averageRating"] = movies.directors.apply(func=returnZero, args={1})
#print(movies["averageRating"])


#-----------SVETA LINIJA KOJA KONACNO RADI----------------------------
# u stupac "directors" dataframea movies transformiramo funkcijom calcDirectros, prvi argument pandas interno salje
# drugi argument funkcije calcDirectros salje sa args={}
movies["directors"] = movies.directors.apply(func=calcDirectors, args={str(series.directors)})
movies["writers"] = movies.writers.apply(func=calcDirectors, args={str(series.writers)})
movies = movies.loc[movies["directors"] != 0]

print(movies[["primaryTitle", "directors", "writers"]])








'''def calcDirectors(movie, series):

    #directors = str(series[["directors"]]).strip().split()
    #other = str(movies[["directors"]]).strip().split()

    directors = str(series[["directors"]]).strip().split()
    other = str(movie.strip().split())


    # micanje smeca, ID-evi direktora,glumaca i pisaca pocinje sa "nm"
    directors = [item for item in directors if "nm" in item]
    other = [item for item in other if "nm" in item]
    temp = set(directors).intersection(other)

    # broj slicnih / broj ukupnih
    # broj ukupnih = suma lista - presijek
    return float(len(temp) / (len(directors) + len(other) - len(temp)))'''