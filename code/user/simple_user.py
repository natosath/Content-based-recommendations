import numpy as np

NUM_GENRES = 26


class SimpleUser:
    def __init__(self, user_id):
        self.user_id = user_id
        # genre : [rating sum, num of ratings]
        self.genres = {'sum': np.zeros(NUM_GENRES), 'watched': np.zeros(NUM_GENRES)}
        # redefine to dict with movie : rating pairs
        self.watched = dict()

    # assumes vectorised genres
    def update(self, series):
        self.genres["sum"] += (series.genres * series.rating * 2)
        self.genres["watched"] += series.genres
        # self.watched.add(str(series.tconst))
        self.watched[str(series.tconst)] = float(series.rating) * 2

    def get_genre_bias(self):
        if self.genres["sum"] is None:
            return 0
        vector = self.genres["sum"]
        divide = self.genres["watched"]
        rez = np.divide(vector, divide, out=np.zeros_like(vector), where=divide != 0)
        return rez

    def __str__(self):
        if self.genres["sum"] is None:
            return "This user hasn't watched any movies yet"
        vector = self.genres["sum"]
        divide = self.genres["watched"]
        rez = np.divide(vector, divide, out=np.zeros_like(vector), where=divide != 0)
        return str(rez)

    def __add__(self, other):
        if self.genres["sum"] is None:
            return 0
        if other.genres["sum"] is None:
            return 0
        if self.user_id == other.user_id:
            return 0
        result = SimpleUser(self.user_id)
        suma = self.genres["sum"] + other.genres["sum"]
        total = self.genres["watched"] + other.genres["watched"]
        watched = self.watched.union(other.watched)
        result.genres["sum"] = suma
        result.genres["watched"] = total
        result.watched = watched
        return result

    # def update(self, series):
    #     rating = float(series.rating)
    #     genres = str(series.genres)
    #     genres = genres.lower()
    #     genres = genres.strip().split(",")
    #     for genre in genres:
    #         if genre not in self.genres.keys():
    #             self.genres[genre] = [0, 0]  # total, num of films
    #         self.genres[genre][0] += rating
    #         self.genres[genre][1] += 1
