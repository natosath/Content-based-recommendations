import pandas as pd

matrix = pd.read_csv('matrix.csv',
                     sep=',',
                     names=['tconst', 'primaryTitle',
                            'startYear', 'runtimeMinutes',
                            'genres', 'directors',
                            'writers', 'actors',
                            'similarity', 'movie'])
matrix.to_csv('matrix.csv')
