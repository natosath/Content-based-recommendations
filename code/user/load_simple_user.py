import pandas as pd
import numpy as np
from code.user.simple_user import SimpleUser
import time
import pickle


# converts genre from str to numpy array of ints
def convert_to_numpy(series):
    array = str(series[1:-1]).strip().replace(",", "").split(" ")
    array = [float(x) for x in array]
    return np.array(array)


# use 300k when doing for real
NUM_OF_USERS = 15_000
CHUNK_SIZE = 30_000
start = time.time()
path_ratings = '/home/natosath/Desktop/Projekt/movie-lens-csv/sorted_rating_with_imdb_id.csv'
path_database = '/home/natosath/Desktop/Projekt/code/refactor_database/gen_normed_np-database.csv'
ratings = pd.read_csv(path_ratings, chunksize=CHUNK_SIZE, low_memory=False, index_col=0)
database = pd.read_csv(path_database, usecols=["tconst", "genres"],
                       dtype={'tconst': str})
database["genres"] = database.genres.apply(func=convert_to_numpy)
# print(database["genres"])

# database.info(verbose=True)
users = dict()


def load_user(series):
    global users
    if max(series.genres) > 1:
        return
    if series.userId not in users.keys():
        users[series.userId] = SimpleUser(int(series.userId))
    users[series.userId].update(series)
    # if max(series.genres) > 1:
    #     print(series.tconst)
    return


def filter_and_pickle(obj, maximum, file):
    for key, value in obj.items():
        if key < maximum:
            pickle.dump(value, file)
    return {key: user for key, user in obj.items() if key >= maximum}


f = open('simple_users.pkl', mode="wb")

max_id = -1
counter = 0
print("starting chunk")
for rating in ratings:
    rating = rating.merge(database, on="tconst")
    rating.apply(func=load_user, axis=1, args={})
    users = filter_and_pickle(users, max_id, f)
    max_id = max(users.keys())
    print("chunk done, ", time.time() - start, " seconds elapsed since start")
    if max_id >= NUM_OF_USERS:
        break
    print("progress: ", (max_id / NUM_OF_USERS) * 100, "%")
    # counter += 1
    # if counter == 6:
    #     break

# print("max id is ", max_id)
# pickle the remaining users

for value in users.values():
    pickle.dump(value, f)

# test unpickle
f.close()
f = open('simple_users.pkl', mode="rb")
ids = []

while 1:
    try:
        user = pickle.load(f)
        ids.append(user.user_id)
        # if min(bias[bias != 0]) < 1:
        #     print(user.genres["sum"])
        #     print(user.genres["watched"])
        #     print(bias)
        #     print(len(user.watched))
        #     print("---------------------------")
    except EOFError:
        break

f.close()
print("len of ids ", len(ids))
print("unique ids", len(set(ids)))

print(time.time() - start, " seconds")
print((time.time() - start) / 60, " minutes")
print((time.time() - start) / 3600, " hours")
