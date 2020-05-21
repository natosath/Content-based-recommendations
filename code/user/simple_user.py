class SimpleUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.genres = dict()

    def update(self, series):
        rating = float(series.rating)
        genres = str(series.genres)
        genres = genres.lower()
        genres = genres.strip().split(",")
        for genre in genres:
            if genre not in self.genres.keys():
                self.genres[genre] = [0, 0]  # total, num of films
            self.genres[genre][0] += rating
            self.genres[genre][1] += 1

    def __str__(self):
        return str(self.genres)
