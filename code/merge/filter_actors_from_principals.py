import pandas as pd


def filter_actors(source, destination):
    read_principals = pd.read_csv(source,
                                  sep="t",
                                  chunksize=200000,
                                  na_values="\\N",
                                  low_memory=False)

    is_first = True

    for principal in read_principals:
        principal = principal.drop(columns=["job"])
        # direktori i pisci se zasebno uzimaju u drugoj datoteci
        principal = principal.loc[principal["category"] == "actor"]
        principal = principal.sort_values(["tconst"])

        if is_first and (not principal.empty):
            principal.to_csv(destination, index=False)
            is_first = False
        elif not principal.empty:
            principal.to_csv(destination, index=False, header=False, mode="a")

        print("CHUNK DONE")

    print("FILTER DONE")

# filter_actors("../title.principals.tsv", '../actors.csv')
