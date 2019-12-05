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

# TODO Solve HORRIBLE inefficiency when using merge function

MIN_VOTE_NUM = 200


def main_mbr():
    global MIN_VOTE_NUM

    basics_reader = pd.read_csv("title.basics.tsv",
                                sep="\t",
                                chunksize=150000,
                                na_values="\\N",
                                low_memory=False)
    ratings = pd.read_csv("title.ratings.tsv",
                          sep="\t",
                          na_values="\\N")
    is_first = True

    for basic in basics_reader:
        basic = basic.drop(columns=["endYear"])
        basic = basic.loc[basic["titleType"] == "movie"]
        basic = basic.sort_values("tconst")
        merged = pd.merge(basic, ratings, how="outer", on="tconst")
        merged = merged.loc[(merged["titleType"].notnull()) &
                            (merged["numVotes"].notnull()) &
                            (merged["averageRating"].notnull()) &
                            (merged["originalTitle"].notnull()) &
                            (merged["numVotes"] > MIN_VOTE_NUM)]
        merged = merged.drop(columns=["titleType"])
        merged = merged.sort_values(["tconst"])

        """if not merged.empty:
            print(merged[["primaryTitle", "averageRating"]])"""
        if is_first and (not merged.empty):
            merged.to_csv('merged.csv', index=False)
            is_first = False
        elif not merged.empty:
            merged.to_csv('merged.csv', index=False, header=False, mode="a")
        """print(merged)"""

    new = pd.read_csv("merged.csv")
    print(new.shape)
    print(new.dtypes)
    print("MBR DONE\n")
