import pandas as pd
import sys

from code.recommender_eval import compare_random, compare_popular, compare_stat, compare_cosine

# path = str(sys.argv[1])

SAMPLE = 7500
USERS = '../user/simple_users.pkl'
n = 200
database = pd.read_csv('../vectorise_database/gen_normed_np-database.csv', usecols=["tconst", "genres"])
matrix = pd.read_csv('../new_matrix.csv')
cosine_matrix = pd.read_csv('../cosine_matrix.csv')

# for i in range(25):
#     compare_random.compare(SAMPLE, USERS, n, database, matrix, )

# for i in range(25):
#     compare_popular.compare(SAMPLE, USERS, n, database, matrix, )

# for i in range(10):
#     compare_stat.compare(SAMPLE, USERS, n, database, matrix)

for i in range(5):
    compare_cosine.compare(SAMPLE, USERS, n, database, matrix, cosine_matrix)
