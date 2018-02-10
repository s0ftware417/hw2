from pprint import pprint
import time
from math import sqrt


def organazize(data): #could possibly implrove time slightly by combining organazize() and read_in()
    train = {}
    temp = {}
    key = data[0][0]
    for entry in data:
        if (key == entry[0]):
            temp[entry[1]] = entry[2]
        else:
            train[key] = temp
            temp = {}  # clear dictionary
            key = entry[0]
            temp[entry[1]] = entry[2]
    train[key] = temp
    return train


def read_in(filename):
    f = open(filename, 'r')
    data = []
    for line in f:
        entry = line.split("\t")[0:3]
        entry[0] = int(entry[0])
        entry[1] = int(entry[1])
        entry[2] = int(entry[2])
        data.append(entry)
    return data


def how_simmilar(a,b):
    sum = 0
    diff = 0
    at_least_one_in_common = False
    if len(a) > len(b):
        for elem in b.keys():
            if elem in a.keys():
                at_least_one_in_common = True
                diff = a[elem] - b[elem]
                sum += diff ** 2

    else:
        for elem in a.keys():
            if elem in b.keys():
                at_least_one_in_common = True
                diff = a[elem] - b[elem]
                sum += diff ** 2

    if at_least_one_in_common:
        distance = sqrt(sum)
        return 1/(1+distance)
    else:
        return -1


def squad(train, k): #finds the nesrest k userd by sommilarity scores
    for elem in train.keys():

    return

def main():
    starttime = time.time()
    data = read_in("u1-base.base")
    train = organazize(data)
    #pprint(train)
    print(how_simmilar(train[2],train[3]))
    print("Runtime was: ", time.time() - starttime)


if __name__ == '__main__': main()