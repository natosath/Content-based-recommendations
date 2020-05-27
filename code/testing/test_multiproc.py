import pandas as pd
import numpy as np
from multiprocessing import Process, cpu_count, Pool
import time
from code import find_similar


# minhash genres with binary arrays using manhatan distance
# TODO writing the file
# or CUDA, pytorch, rapids ai

# film_ids, database, how_many
def similar_for_id(args):
    film_ids, database, how_many = args[0], args[1], args[2]
    for film in film_ids:
        find_similar.find_most_similar(film, database, how_many)
        print(film)


def foo(one):
    print(one[0], one[1])


# somethings wrong with using pool
if __name__ == '__main__':
    start = time.time()
    workers = cpu_count() - 1
    HOW_MANY_FILMS = 3
    HOW_MANY_SIMILAR = 40
    processes = []
    nodes = []
    database = pd.read_csv("database.csv")
    film_ids = np.array_split(database["tconst"], workers)
    for ids in film_ids:
        nodes.append([ids, database, HOW_MANY_FILMS])
    with Pool(processes=workers) as pool:
        bar = pool.imap(similar_for_id, nodes)
    # p = Pool(processes=workers)
    # p.imap(similar_for_id, nodes)

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


# def print_head(n):
#     for i in range(2 * n):
#         print(n - 1, i ** i)
#
#
# if __name__ == '__main__':
#     procs = []
#     workers = cpu_count()
#
#     for i in range(workers):
#         p = Process(target=print_head, args=(i + 1,))
#         procs.append(p)
#         p.start()
#     # procs.reverse()
#
#     # for pro in procs:
#     # pro.target = print_head
#     # pro.args = (100,)
#
#     for pro in procs:
#         pro.join()
