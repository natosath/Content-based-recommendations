import pandas as pd

# verzija baze je ~20.10.2019
# ovdje cu spojiti datoteke
# filtriram van : bilo kakav ne-film
# uzimam filmove sa 200 ili vise ratinga radi preciznosti


"""
#
#
#
#
"""



def merge_bnr_crew(crew, bnr, destination):
    MIN_VOTE_NUM = 200
    print("Merging with crew...")

    crew_reader = pd.read_csv(str(crew),
                              sep="\t",
                              chunksize=150000,
                              na_values="\\N",
                              low_memory=False)
    test = pd.read_csv(str(bnr))
    is_first = True

    for crew in crew_reader:
        crew = crew.sort_values(["tconst"])
        final = pd.merge(test, crew, how="inner", on="tconst")
        final = final.loc[(final["averageRating"].notnull()) &
                          (final["writers"].notnull())]
        final = final.sort_values(["tconst"])
        if is_first and (not final.empty):
            final.to_csv(str(destination), index=False)
            is_first = False
        elif not final.empty:
            final.to_csv(str(destination), index=False, header=False, mode="a")
        """if not final.empty:
            print(final)"""

    new = pd.read_csv(str(destination))
    print(new.shape)
    print(new.dtypes)
    print("MERGED BASICS&RATINGS WITH CREW!")
    print("++++++++++++++++++++++++++++++++++\n")
