from time import sleep
import pandas as pd
import numpy as np
from multiprocessing import Process, cpu_count, Queue
import time
from code import find_similar


# minhash genres with binary arrays using manhatan distance
# TODO version where each worker also writers
# or CUDA, pytorch, rapids ai


def similar_for_id(film_ids, database, how_many, que):
    for film in film_ids:
        similars = find_similar.find_most_similar(film, database, how_many)
        similars["movie"] = film
        que.put(similars)
    que.put(None)
    # print(similars)


def write_to_target(target, que, workers):
    while (workers > 0):
        if not que.empty():
            foo = que.get()
            if foo is None:
                workers -= 1
            else:
                foo.to_csv(target, index=False, header=False, mode="a")


if __name__ == '__main__':
    start = time.time()
    workers = cpu_count() - 1
    HOW_MANY_FILMS = 3
    HOW_MANY_SIMILAR = 40
    processes = []
    to_write = Queue(maxsize=0)
    cols = ['tconst', 'primaryTitle', 'isAdult',
            'startYear', 'runtimeMinutes', 'genres',
            'directors', 'writers', 'actors']
    database = pd.read_csv("database.csv", usecols=cols)
    # matrix = pd.read_csv('matrix.csv')
    matrix = 'matrix.csv'
    film_ids = np.array_split(database["tconst"], workers)
    for i in range(workers):
        p = Process(target=similar_for_id, args=(film_ids[i].head(HOW_MANY_FILMS),
                                                 database,
                                                 HOW_MANY_SIMILAR,
                                                 to_write,))
        processes.append(p)
        p.start()

    writer = Process(target=write_to_target, args=(matrix,
                                                   to_write,
                                                   workers))
    writer.start()

    for process in processes:
        process.join()

    writer.join()

    # here will be adjusting the matrix
    # adjusting the index and rearranging columns

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
