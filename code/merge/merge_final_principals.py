import pandas as pd


def main_mfp():
    principals = pd.read_csv("title.principals.tsv",
                             sep="\t",
                             chunksize=150000,
                             na_values="\\N",
                             low_memory=False)

    final = pd.read_csv("final.csv")

    for prin in principals:
        print(prin)
