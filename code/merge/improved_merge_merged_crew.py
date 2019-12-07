import pandas as pd

# verzija baze je ~20.10.2019
# ovdje cu spojiti datoteke
# filtriram van : bilo kakav ne-film
# uzimam filmove sa 200 ili vise ratinga radi preciznosti


"""
#
# main_mbr()
#
# Filters out anything that is not a film out of title.basics.tsv
  Filters out movies who have less than MIN_VOTE_NUM votes as they may
  not have sufficient data.
  Merges title.basics.tsv with title.ratings.tsv by tconst which serves as an ID

#
"""

MIN_VOTE_NUM = 200


def main_mmc():
    global MIN_VOTE_NUM

    crew_reader = pd.read_csv("title.crew.tsv",
                              sep="\t",
                              chunksize=150000,
                              na_values="\\N",
                              low_memory=False)
    test = pd.read_csv('merged.csv')
    is_first = True

    for crew in crew_reader:
        crew = crew.sort_values(["tconst"])
        final = pd.merge(test, crew, how="inner", on="tconst")
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

    new = pd.read_csv("final.csv")
    print(new.shape)
    print(new.dtypes)
    print("MMC DONE\n")
