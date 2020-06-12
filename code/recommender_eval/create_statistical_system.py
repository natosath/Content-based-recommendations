# TODO make dict with (movie,movie) : frequency pairs
import pickle
import time
import pandas as pd
import time

start = time.time()
read = open('../user/simple_users.pkl', mode="rb")
write = open('movie_relations.pkl', mode="wb")
frequency = dict()
NUM_OF_USERS = 15_000
count = 0
first = False
while 1:
    try:
        user = pickle.load(read)
        movies = sorted(user.watched)
        while movies:
            current = movies.pop(0)
            if len(movies) == 0:
                break
            for movie in movies:
                if current == movie:
                    continue
                key = sorted([current, movie])
                key = key[0] + "," + key[1]
                if key not in frequency.keys():
                    frequency[key] = 0
                frequency[key] += 1
    except EOFError:
        break
    count += 1
    if count % 10 == 0:
        print("progress: ", count * 100 / NUM_OF_USERS, "% ",
              time.time() - start, " seconds elapsed")

    if count % 30 == 0:
        df = pd.DataFrame.from_dict(frequency, orient="index", columns=["value"])
        df = df.reset_index(drop=False)
        pickle.dump(df, write)
        frequency = dict()
        if count % 1800 == 0:
            break

        # holy lines for later
        # df = pd.concat([df, df])
        # df = df.groupby(by="index")["value"].sum()

        # if first:
        #     df.to_csv('test.csv', mode="w")
        #     first = False
        # else:
        #     df.to_csv('test.csv', mode="a", header=False)

        # df = pd.read_csv('test.csv', index_col=0)


write.close()
# for key, value in frequency.items():
#     if value > 5:
#         print(key, value)


# def combine(first, second):
#     print(first.dropna())
#     print(second)
#     print("end func")
#     # rez = pd.Series({'first': first[1].first,
#     #                  'second': first[1].second,
#     #                  'value': first[1].value + second[1].value})
#     return 0


# df = pd.DataFrame.from_dict(frequency, orient="index", columns=["value"])
# df = df.reset_index(drop=False)
# df["movies"] = df["index"]

# df["first"] = df.apply(func=get_movie, axis=1, args=(0,))
# df["second"] = df.apply(func=get_movie, axis=1, args=(1,))
# df["first"] = df["movies"][0]

# df = df.loc['tt0112579' in df["movies"]]
# df[['first', 'second']] = pd.DataFrame(df['index'].tolist(), index=df.index)
# df = df.drop(columns="movies")
# df = df.drop(columns="index")
# print(df.shape)
# test = pd.merge(df[500:1500], df[0:1000], on="index", how="outer")
# test = df.loc[500:1500].add(df.loc[0:1000], fill_value=0, axis="columns")

# test = test.groupby("index")["value"].sum()

# new_dict = {key[0] + "," + key[1]: value for key, value in frequency.items()}
# df = pd.DataFrame.from_dict(new_dict, orient="index", columns=["value"])
# df = df.reset_index(drop=False)

# holy lines
# ----
# test = pd.concat([df[0:1000], df[500:1500]])
# test2 = pd.concat([df[100:1100], df[700:1700]])
# test = test.groupby("index")["value"].sum()
# tes2 = test2.groupby("index")["value"].sum()
# test = pd.concat([test2])
# test = test.groupby("index").sum()

# test = test.dropna()
# print(test[test.value > 2])
# print(test)
# print(type(test))
# print(df.shape)
# print(df)
# print(test.shape)
print("time: ", time.time() - start, " seconds")

# print(test.loc[501])
# print(df.loc[501])
