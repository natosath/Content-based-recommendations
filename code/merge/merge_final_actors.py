import pandas as pd


def merge_final_with_actors(final, actors, destination):
    actors_reader = pd.read_csv(actors,
                                sep=",",
                                chunksize=150000,
                                na_values="\\N",
                                low_memory=False)

    final = pd.read_csv(final,
                        sep=",",
                        na_values="\\N")
    is_first = True

    for actor in actors_reader:
        joined = pd.merge(final, actor, how="inner", on="tconst")
        print(joined)

        if is_first and (not joined.empty):
            joined.to_csv(str(destination), index=False)
            is_first = False
        elif not joined.empty:
            joined.to_csv(str(destination), index=False, header=False, mode="a")


merge_final_with_actors('../final.csv', '../actors.csv', '../database.csv')
