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
    count = 0
    at_least_one_in_common = False
    if len(a) > len(b):
        for elem in b.keys():
            if elem in a.keys():
                count += 1
                at_least_one_in_common = True
                diff = a[elem] - b[elem]
                sum += diff ** 2

    else:
        for elem in a.keys():
            if elem in b.keys():
                count += 1
                at_least_one_in_common = True
                diff = a[elem] - b[elem]
                sum += diff ** 2

    if at_least_one_in_common:
        distance = sqrt(sum)
        return 1/(1+distance) + count * .001 # this makes it so that for two users
    else:
        return -1


def how_simmilar_v2(a,b):
    sum = 0
    diff = 0
    count = 0
    at_least_one_in_common = False
    if len(a) > len(b):
        for elem in b.keys():
            if elem in a.keys():
                count += 1
                at_least_one_in_common = True
                diff = abs(a[elem] - b[elem])
                sum += (5 - diff)/5
    else:
        for elem in a.keys():
            if elem in b.keys():
                count += 1
                at_least_one_in_common = True
                diff = abs(a[elem] - b[elem])
                sum += (5 - diff) / 5

    if at_least_one_in_common:
        return sum
    else:
        return -1


def squad(train, user_num, k): #finds the nesrest k userd by sommilarity scores
    all_sim = []
    dream_team = []
    for elem in train.keys():
        if elem != user_num:
            friendly_neighborhood_tuple = (how_simmilar_v2(train[user_num], train[elem]), elem)
            all_sim.append(friendly_neighborhood_tuple)
    top_k = sorted(all_sim, reverse=True)[0:k]
    return top_k


def unison(u1, u2):
    uni = []
    for mov in u1.keys():
        uni.append(mov)
    for mov in u2.keys():
        if mov not in uni:
            uni.append(mov)
    return uni

def main():
    starttime = time.time()
    data = read_in("u1-base.base")
    train = organazize(data)
    #pprint(train)
    #top = squad(train, 1, 2)
    #pprint(top)
    print("Runtime was: ", time.time() - starttime)


if __name__ == '__main__': main()