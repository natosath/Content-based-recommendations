import pickle

print("unpickling")
with open("pickle_test.pkl", "rb") as test:
    users = pickle.load(test)
for key, value in users.items():
    print(key, value)
print("num of users ", len(users.keys()))
print("max user id ", max(users.keys()))

# print(users)
