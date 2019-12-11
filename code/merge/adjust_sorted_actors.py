import pandas as pd


def fix_actors(actors):
    actors = actors.split("nm")
    # remove empty strings
    actors = list(filter(None, actors))
    # gives back "nm" prefix to actors
    for i in range(len(actors)):
        actors[i] = "nm" + actors[i]
    return actors


def adjust_sorted_actors(source, destination):
    actor_reader = pd.read_csv(source,
                               sep=",",
                               chunksize=150000,
                               na_values="\\N",
                               low_memory=False)

    is_first = True

    for actor in actor_reader:
        actor["actors"] = actor.actors.apply(func=fix_actors, args={})
        print(actor)
        print(actor.dtypes)

        if is_first and (not actor.empty):
            actor.to_csv(str(destination), index=False)
            is_first = False
        elif not actor.empty:
            actor.to_csv(str(destination), index=False, header=False, mode="a")


# adjust_sorted_actors('../sorted.actors.csv', '../actors.csv')
