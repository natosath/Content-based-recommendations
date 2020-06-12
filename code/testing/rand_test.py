import pandas as pd


def sims(series):
    return "foo"


# shawshank tt0111161

database = pd.read_csv('../database.csv')
cell = database["tconst"].values.tolist()
database["test"] = database.apply(func=sims, axis=1, args={})
new = pd.DataFrame()
new["tconst"] = database["tconst"]
new["test"] = database["test"]
# print(database.head(10))
database.info(verbose=True)
print(database.shape)

database = database.drop(columns=["test"])
print(database.shape)
nans = database[database.isna().any(axis=1)]
print(nans["primaryTitle"].head(100))

new = database[["tconst", "primaryTitle"]]
print(new)
new.info()
