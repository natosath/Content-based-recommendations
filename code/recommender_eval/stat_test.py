from collections import Counter
import pandas as pd
import pickle
import random
import time

start = time.time()

bar = [[1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2, 3, 3, 3], [1, 1, 2, 2, 2, 3, 3, 3], {1, 4, 6}]
counter = Counter()
USERS = '../user/simple_users.pkl'

df = pd.read_csv('../vectorise_database/gen_normed_np-database.csv')

users = []
count = 0
n = 200
file = open(USERS, mode="rb")
while 1:
    try:
        user = pickle.load(file)
        users.append(user)

        # if random.randint(0, 5) == 0:
        #     users.append(user)
        #     count += 1
    except EOFError:
        break
    # if count >= n:
    #     break
file.close()
seek = time.time()
# for user in users:
#     if 'tt0110475' in user.watched:
#         counter.update(user.watched)
filtered = [user for user in users if 'tt0111161' in user.watched]
for user in filtered:
    counter.update(user.watched)
print("seek time : ", time.time() - seek)
common = counter.most_common(20 + 1)
print(common)
common = [x[0] for x in common[1:]]
print(common)

# df[df.countries.isin(countries)]
df = df[df.tconst.isin(common)]
print(df.primaryTitle.equals.tolist())

print("program end in ", time.time() - start)
