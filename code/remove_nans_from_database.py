import pandas as pd

database = pd.read_csv('database.csv', index_col=0)
database.info(verbose=True)
database = database.dropna(axis=0)
print(database.shape)
database.info(verbose=True)
database.to_csv('new_database.csv', mode="w")
