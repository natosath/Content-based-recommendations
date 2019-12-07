import pandas as pd


def main_adjust():
    final = pd.read_csv("final.csv")

    #final["popularPower"] = np.log2(np.log2(final["averageRating"]) * np.log10(final["numVotes"]) + 1)
    #final["popularPower"] = np.round(final["popularPower"], decimals=3)
    final = final.sort_values(["tconst", "primaryTitle", "averageRating"])
    print(final)
    final.to_csv("final.csv", index=False)

    #final = pd.read_csv("final.csv")
    #final = final.sort_values(["popularPower"])
    #print(final)
    #print(final[["primaryTitle", "averageRating", "popularPower"]].tail(5))
    print("AF DONE\n")


