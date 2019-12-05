import pandas as pd

# TODO Solve HORRIBLE inefficiency when using merge function

def main_mmc():
    is_first = True

    crew_reader = pd.read_csv("title.crew.tsv",
                              sep="\t",
                              chunksize=150000,
                              na_values="\\N",
                              low_memory=False)

    merged = pd.read_csv("merged.csv")

    for crew in crew_reader:
        crew = crew.sort_values(["tconst"])
        final = pd.merge(merged, crew, how="outer", on="tconst")
        final = final.loc[(final["averageRating"].notnull()) &
                          (final["writers"].notnull())]
        final = final.sort_values(["tconst"])
        if is_first and (not final.empty):
            final.to_csv('final.csv', index=False)
            is_first = False
        elif not final.empty:
            final.to_csv('final.csv', index=False, header=False, mode="a")
        """if not final.empty:
            print(final)"""

    print(merged.shape)
    print(merged.dtypes)
    new = pd.read_csv("final.csv")
    print(new.shape)
    print(new.dtypes)
    print("MMC DONE\n")


