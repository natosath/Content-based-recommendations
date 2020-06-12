import pickle as pk


def get_genre_vector(path):
    with open(path, mode="rb") as file:
        genres = pk.load(file)
        return genres
