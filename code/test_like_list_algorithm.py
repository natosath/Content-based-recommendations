first = ["lalal", "nm42", "hoho", "nm69", "nyeh"]
second = ["lalal", "nm42", "nm12", "nm69", "nyeh", "ne"]
third = ["lalal", "nm42", "hoho", "nm69", "nm99", "nm12", "zen"]


def similarity(prvi, drugi):
    prvi = [item for item in prvi if "nm" in item]
    drugi = [item for item in drugi if "nm" in item]
    temp = set(prvi).intersection(drugi)
    #print("nakon filtra")
    #print(prvi, drugi, temp)
    #print(len(prvi),len(drugi),len(temp))

    # broj slicnih / broj ukupnih
    # broj ukupnih = suma lista - presijek
    rez = float(len(temp) / (len(prvi) + len(drugi) - len(temp)))
    return rez

print(similarity(first,second))
print(similarity(first,third))
print(similarity(second,third))