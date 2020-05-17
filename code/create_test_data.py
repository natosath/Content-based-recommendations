import pandas as pd

db = dict()
link = dict()


def trunc_tconst(series):
    global db
    temp = len(series.tconst[2:])
    if temp not in db.keys():
        db[temp] = 0
    else:
        db[temp] += 1
    return series.tconst[2:]


def fill_with_zero(ids):
    if len(ids) == 7:
        return ids
    zeros = 7 - len(ids)
    zeros = "0" * zeros
    return zeros + ids


def to_string(series):
    global link
    temp = len(str(series.tconst))
    if temp not in link.keys():
        link[temp] = 0
    else:
        link[temp] += 1
    return fill_with_zero(str(series.tconst))


destination = 'test_database.csv'
database = pd.read_csv('database.csv')
database['tconst'] = database.apply(func=trunc_tconst, axis=1, args={})
links = pd.read_csv('links.csv', usecols=['imdbId'])
links = links.rename(axis=1, mapper={'imdbId': 'tconst'})
links['tconst'] = links.apply(func=to_string, axis=1, args={})

test = database.merge(links, how="inner")
# print(database.tconst)
# print(links.tconst)
# print(test.tconst)
# print(database.shape)
print(test.shape)
# print(db, link)
test.to_csv(destination, index=False)
test = pd.read_csv(destination)
test = test.sort_values(by=["averageRating"], ascending=False)
print(test[["primaryTitle", "averageRating", "numVotes"]].head(100), test.shape)
