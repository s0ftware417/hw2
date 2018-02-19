from pprint import pprint
import time
from math import sqrt
from tqdm import tqdm

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


def how_simmilar_v2(a, b):
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
        return .00001


def euclidean(a, b):
    sum = 0
    for elem in a.keys():
        if elem in b.keys():
            sum += (a[elem]-b[elem])**2
        else:
            sum += a[elem]**2
    for elem in b.keys():
        if elem not in a.keys():
            sum += b[elem]**2
    if sum <= 0:
        return 0
    else:
        return sqrt(sum)


def squad(train, user_num, movie_num, k): #finds the nesrest k userd by sommilarity scores
    all_sim = []
    dream_team = []
    for elem in train.keys():
        if elem != user_num:
            if movie_num in train[elem].keys():
                friendly_neighborhood_tuple = (how_simmilar_v2(train[user_num], train[elem]), elem)
                all_sim.append(friendly_neighborhood_tuple)
    top_k = sorted(all_sim, reverse=True)[0:k] #need to handle case where there arent k in all_sim
    return top_k


def predickt(nearest, train, movie):
    sum = 0
    for user in nearest:
        sum += train[user[1]][movie]
    if len(nearest) <= 0:
        return 2.5
    else:
        return sum/len(nearest)

def predickt_v2(nearest, train, movie):
    #pprint(nearest)
    if len(nearest) <= 0:
        return 2.5
    elif len(nearest) == 1:
        return train[nearest[0][1]][movie]
    else:
        sum = 0
        denom = 0
        for user in nearest:
            denom += user[0]
        for user in nearest:
            weighted = 1 - (user[0]/denom)
            sum += (train[user[1]][movie]*weighted)/weighted
        #print(sum)
        return sum/10


def test_prediction(train):
    test = read_in("u1-test.test")
    #pprint(test)
    sum = 0
    for elem in tqdm(test):
        guess = predickt(squad(train, elem[0], elem[1], 10), train, elem[1])
        actual = elem[2]
        sum += (guess - actual)**2
    print("MSE =", sum/len(test))

def test_prediction_k_loop(train, min, max):
    test = read_in("tryme.txt")
    # pprint(test)
    results = []
    for k in tqdm(range(min, max+1)):
        sum = 0
        for elem in test:
            guess = predickt(squad(train, elem[0], elem[1], k), train, elem[1])
            actual = elem[2]
            sum += (guess - actual) ** 2
        MSE = sum / len(test)
        tuple = (k,MSE)
        results.append(tuple)
    return results

def main():
    data = read_in("u1-base.base")
    train = organazize(data)
    #print(euclidean(train[2], train[1]))
    starttime = time.time()
    pprint(test_prediction_k_loop(train, 5, 10))
    #movie = 122
    #top = squad(train, 1, movie, 3)
    #print(predickt(top,train,movie))
    #print(top)
    print("Runtime was: ", time.time() - starttime)


if __name__ == '__main__': main()