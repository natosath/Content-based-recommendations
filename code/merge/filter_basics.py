import pandas as pd


def filter_basics():
    basics = pd.read_csv("title.basics.tsv",
                         sep="\t",
                         chunksize=150000,
                         na_values="\\N",
                         low_memory=False)

    is_first = True

    for basic in basics:

        basic = basic.drop(columns=["endYear"])
        # removing anything that is not a movie
        basic = basic.loc[basic["titleType"] == "movie"]
        basic = basic.loc[basic["genres"].notnull()]
        basic = basic.sort_values("tconst")

        if is_first and (not basic.empty):
            basic.to_csv('basic.csv', index=False)
            is_first = False
        elif not basic.empty:
            basic.to_csv('basic.csv', index=False, header=False, mode="a")

    print("FILTER DONE")
