import pandas as pd

path = '/home/natosath/Desktop/Projekt/code/database.csv'
database = pd.read_csv(path,
                       usecols=['tconst', 'primaryTitle', 'originalTitle', 'isAdult',
                                'startYear', 'runtimeMinutes', 'genres', 'averageRating', 'numVotes',
                                'directors', 'writers', 'actors'])
print(database.columns)
database.reindex()
database.to_csv(path)
