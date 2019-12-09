import pandas as pd


def adjust_final(final):
    print("Adjusting final...")
    print("Reading final")
    final = pd.read_csv(final)
    print("Reading final DONE")

    #final["popularPower"] = np.log2(np.log2(final["averageRating"]) * np.log10(final["numVotes"]) + 1)
    #final["popularPower"] = np.round(final["popularPower"], decimals=3)
    print("Sorting final")
    final = final.sort_values(["tconst", "primaryTitle", "averageRating"])
    print("Sorting final DONE")
    print(final)
    print("Writing final")
    final.to_csv('final.csv', index=False)
    print("Writing final DONE")

    #final = pd.read_csv("final.csv")
    #final = final.sort_values(["popularPower"])
    #print(final)
    #print(final[["primaryTitle", "averageRating", "popularPower"]].tail(5))
    print("ADJUSTED FINAL")


