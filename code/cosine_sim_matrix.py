from time import sleep
import pandas as pd
import numpy as np
from multiprocessing import Process, cpu_count, Queue
import time
from code import cosine_find_similar


# minhash genres with binary arrays using manhatan distance
# TODO version where each worker also writers
# or CUDA, pytorch, rapids ai


def similar_for_id(film_ids, database, how_many, que):
    for film in film_ids:
        similars = cosine_find_similar.find_most_similar(film, database, how_many)
        # similars["movie"] = film
        que.put(similars)
    que.put(None)
    # print(similars)


def write_to_target(target, que, workers):
    first = True
    while (workers > 0):
        if not que.empty():
            foo = que.get()
            if foo is None:
                workers -= 1
            elif not foo.empty:
                if first:
                    foo.to_csv(target, index=False, mode="a")
                    first = False
                else:
                    foo.to_csv(target, index=False, header=False, mode="a")


if __name__ == '__main__':
    start = time.time()
    workers = cpu_count() - 1
    FILMS_PER_WORKER = 2500
    TAKE_TOP_SIMILAR = 20
    processes = []
    to_write = Queue(maxsize=0)
    cols = ['tconst', 'primaryTitle', 'isAdult',
            'startYear', 'runtimeMinutes', 'genres',
            'directors', 'writers', 'actors']
    database = pd.read_csv("new_database.csv", usecols=cols)
    sample = database.head(workers * FILMS_PER_WORKER)  # our dataset for which we will fill matrix
    # print(database)
    # film_ids[i].head(FILMS_PER_WORKER)
    # matrix = pd.read_csv('matrix.csv')
    destination = 'cosine_matrix.csv'
    film_ids = np.array_split(sample["tconst"], workers)
    for i in range(workers):
        p = Process(target=similar_for_id, args=(film_ids[i],
                                                 database,
                                                 TAKE_TOP_SIMILAR,
                                                 to_write,))
        processes.append(p)
        p.start()

    writer = Process(target=write_to_target, args=(destination,
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
    print("program complete in:", duration / 60, " minutes")
    print("films done: ", workers * FILMS_PER_WORKER)
    print("number of worker processes: ", workers)
    print("per film: ", duration / (FILMS_PER_WORKER * workers), " seconds (effective)")

