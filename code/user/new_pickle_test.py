import pickle

f = open('simple_users.pkl', mode="rb")
ids = []

while 1:
    try:
        user = pickle.load(f)
        ids.append(user.user_id)
        print(max(user.get_genre_bias()), min(user.get_genre_bias()),len(user.watched))
        # if min(bias[bias != 0]) < 1:
        #     print(user.genres["sum"])
        #     print(user.genres["watched"])
        #     print(bias)
        #     print(len(user.watched))
        #     print("---------------------------")
    except EOFError:
        break

# print(users)
