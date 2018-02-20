from pprint import pprint  #god bless whoever made this
import time  #I wish I could import more of this into my weekend...
from math import sqrt  #gotta have sqrt
from tqdm import tqdm  #this is the best thing ever

def organazize(data): #could possibly implrove time slightly by combining organazize() and read_in() but its been a long week
    train = {}  #my outer dictionary
    temp = {}  #my temporary inner dictionary
    key = data[0][0]
    for entry in data:
        if (key == entry[0]):
            temp[entry[1]] = entry[2]
        else:
            train[key] = temp
            temp = {}  # clear dictionary
            key = entry[0]
            temp[entry[1]] = entry[2]
    train[key] = temp #catches the last user
    return train


def read_in(filename):  #reads in filename and puts it into an array of arrays called data
    f = open(filename, 'r')
    data = []
    for line in f:
        entry = line.split("\t")[0:3]
        entry[0] = int(entry[0])
        entry[1] = int(entry[1])
        entry[2] = int(entry[2])
        data.append(entry)
    return data


def how_similar(a,b): #initial version of my similarity function. doesn't even work now... but I keep it here to remember where i came from. never forget...
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


def how_similar_v2(a, b):
    sum = 0
    diff = 0
    count = 0
    at_least_one_in_common = False
    if len(a) > len(b):  #me trying to be clever by running the shorter of the two loops
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
        return .00001 #this way i dont run into a divide by zero error, keeps eberything above 0


def how_similar_v3(a, b):
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
                sum += 1 / (2 ** diff)
    else:
        for elem in a.keys():
            if elem in b.keys():
                count += 1
                at_least_one_in_common = True
                diff = abs(a[elem] - b[elem])
                sum += 1 / (2 ** diff)

    if at_least_one_in_common:
        return sum
    else:
        return .00001 #this way i dont run into a divide by zero error, keeps eberything above 0


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


def squad_up_boyzzz(train, user_num, movie_num, k): #finds the nesrest k userd by sommilarity scores
    all_sim = []
    for elem in train.keys():
        if elem != user_num: #in leave one out crossvalidation this is the line that leaves it out... rather redundant but true
            if movie_num in train[elem].keys():
                friendly_neighborhood_tuple = (how_similar_v3(train[user_num], train[elem]), elem)
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
            sum += (train[user[1]][movie]*(user[0]/denom))
        return sum


def predickt_eu(nearest, train, movie):
    if len(nearest) <= 0:
        return 2.5
    elif len(nearest) == 1:
        return train[nearest[0][1]][movie]
    else:
        sum = 0
        denom = 0
        frac = 0
        we_tot = 0
        weight = 0
        for user in nearest:
            denom += user[0]
        for user in nearest:
            weight = 1- (user[0]/denom)
            we_tot += weight
            sum += weight * train[user[1]][movie]
        frac = 1/we_tot
        final = frac*sum
        #print("?", final)
        return final


def prediction(train, k, filename): #this loop runs once for one k value
    test = read_in(filename)
    sum = 0
    for elem in tqdm(test):
        guess = predickt_v2(squad_up_boyzzz(train, elem[0], elem[1], k), train, elem[1])  #version check: make sure youre on the right version so you dont waste 2 hours trying to figure out whats wrong...
        actual = elem[2]
        sum += (guess - actual)**2
    tuple_to_the_rescue = (k, sum/len(test))
    return tuple_to_the_rescue


def prediction_k_loop(train, min, max, filename):  #same as test_predicktion only it runs for a range of k values
    test = read_in(filename)
    results = []
    for k in range(min, max+1):  #this is how i do the leave one out. see more in squad_up_boyzzz() line 4
        sum = 0
        for elem in tqdm(test):
            guess = predickt_v2(squad_up_boyzzz(train, elem[0], elem[1], k), train, elem[1])  #version check part 2
            actual = elem[2]
            sum += (guess - actual) ** 2
        MSE = sum / len(test)
        tuple = (k,MSE)
        results.append(tuple)
    return results #k-value index 0 resulting error index 1


def main():
    data = read_in("u1-base.base")
    train = organazize(data)
    starttime = time.time()
    answers = prediction(train, 3, "u1-test.test")
    #answers = prediction_k_loop(train, 14, 16, "u1-base.base")
    pprint(answers)
    print("Runtime was: ", time.time() - starttime)


if __name__ == '__main__': main()