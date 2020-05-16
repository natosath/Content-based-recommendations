import pandas as pd
import numpy as np
from multiprocessing import Process, cpu_count
import time
from code import find_similar


# minhash genres with binary arrays using manhatan distance
# TODO GPU computing!!!
# TODO CuPy
# TODO actually write down matrix
# or CUDA, pytorch, rapids ai


def similar_for_id(film_ids, database, how_many):
    for film in film_ids:
        find_similar.find_most_similar(film, database, how_many)


if __name__ == '__main__':
    start = time.time()
    workers = cpu_count() - 1
    HOW_MANY_FILMS = 100
    HOW_MANY_SIMILAR = 40
    processes = []
    database = pd.read_csv("database.csv")
    film_ids = np.array_split(database["tconst"], workers)
    for i in range(workers):
        p = Process(target=similar_for_id, args=(film_ids[i].head(HOW_MANY_FILMS),
                                                 database,
                                                 HOW_MANY_SIMILAR))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    duration = time.time() - start
    print("program complete in:", duration, " seconds")
    print("films done: ", workers * HOW_MANY_FILMS)
    print("workers exploited in poor working conditions: ", workers)
    print("per film: ", duration / (HOW_MANY_FILMS * workers), " seconds (effective)")

# df = pd.read_csv('database.csv')
# tconst = df["tconst"]
# dfs = np.array_split(tconst, 3)
# for t in dfs:
#     print(t.shape)
