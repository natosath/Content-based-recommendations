import pandas as pd

""" 
#
# sort_actors(source, destination)
#
# parameter source is path to file from which we extract actors
# parameter destination is path to file in which we shall write the actors by film
#
#
"""

# TODO Improve slow performance
# TODO Problem line is "actors_by_film = actor.groupby("tconst").nconst.sum()"

def sort_actors(source, destination):
    columns = ["tconst", "nconst"]
    read_actors = pd.read_csv(source,
                              sep=",",
                              chunksize=100000,
                              na_values="\\N",
                              low_memory=False,
                              usecols=columns)

    header = ["actors"]

    is_first = True

    for actor in read_actors:

        actors_by_film = actor.groupby("tconst").nconst.sum()

        print("UNIQUE tconst!")
        print(actors_by_film)
        print("-------------------------\n")

        if is_first and (not actors_by_film.empty):
            actors_by_film.to_csv(str(destination), header=header)
            is_first = False
        elif not actors_by_film.empty:
            actors_by_film.to_csv(str(destination), header=False, mode="a")

# sort_actors('../raw.actors.csv', '../sorted.raw.actors.csv')
