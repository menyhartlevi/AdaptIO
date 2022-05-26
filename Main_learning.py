from GameMaster import GameMaster
import os
import numpy as np
import re
import random
import time


def fittness_find(log_loc):
    logfile = open(log_loc, 'r')
    last = str(logfile.readlines()[-1])
    sizes_index = [m.start() for m in re.finditer('size', last)]
    sizes_near = [0] * len(sizes_index)
    sizes_dot = [0] * len(sizes_index)
    sizes = [0] * len(sizes_index)
    for i in range(len(sizes_index)):
        sizes_near[i] = last[sizes_index[i]:sizes_index[i] + 35]
        sizes_dot[i] = sizes_near[i].find('.')
        sizes[i] = int(sizes_near[i][7:sizes_dot[i]])
    return sizes

def picker(list):
    max = sum(list)
    random_fittness = random.uniform(0, max)
    current = 0
    index = 0
    for i in range(len(list)):
        index += 1
        current += list[i]
        if current > random_fittness:
            return index

def toBinary(n):
    if(n > 1 or n < 0):
        #print(n)
        return "ERROR1"
    answer = ""
    answer = answer + "."
    while 1:
        if(len(answer) > 32):
            return answer
        b = n * 2
        if (b >= 1):
            answer = answer + "1"
            n = b - 1
        else:
            answer = answer + "0"
            n = b
    return answer

def toDecimal(n):
    answer = 0
    #print(n)
    for i in range(len(n)-1):
        answer += int(n[i+1]) * (2 ** (-i-1))
    return answer



"""
weights1 = np.random.random((8, 1))
weights2 = np.random.random((8, 1))
weights3 = np.random.random((8, 1))
weights4 = np.random.random((8, 1))
weights5 = np.random.random((8, 1))
weights6 = np.random.random((8, 1))
weights7 = np.random.random((8, 1))
weights8 = np.random.random((8, 1))
weights9 = np.random.random((8, 1))
weights10 = np.random.random((8, 1))
weights_act = np.random.random((8, 1))


np.savetxt("weights1.txt", weights1)
np.savetxt("weights2.txt", weights2)
np.savetxt("weights3.txt", weights3)
np.savetxt("weights4.txt", weights4)
np.savetxt("weights5.txt", weights5)
np.savetxt("weights6.txt", weights6)
np.savetxt("weights7.txt", weights7)
np.savetxt("weights8.txt", weights8)
np.savetxt("weights9.txt", weights9)
np.savetxt("weights10.txt", weights10)
np.savetxt("weights_act.txt", weights_act)

"""

epochs = 1
repeat = 1
population = 1
mutation = 0.05

fittness = [None] * population
avg_fittness = np

if __name__ == "__main__":


    for k in range(epochs):
        print(str(k+1) + '. epoch')
        for i in range(population):

            actual_weightsfile = 'weights' + str(i + 1) + '.txt'
            weights_act = np.loadtxt(actual_weightsfile)
            np.savetxt("weights_act.txt", weights_act)
            fittness[i] = 0
            for z in range(repeat):
                gm = GameMaster()
                time.sleep(5)
                gm.run()
                gm.close()
                fittness[i] = fittness[i] + fittness_find('C:\\Users\\menyh\\repos\\adaptivegame\\log\\adaptio_log_.txt')[2]

            print(fittness)

        picks_1 = [None] * population
        picks_2 = [None] * population

        for i in range(population):
            picks_1[i] = picker(fittness)
            picks_2[i] = picker(fittness)

            parent_1_filename = 'weights' + str(picks_1[i]) + '.txt'
            parent_2_filename = 'weights' + str(picks_2[i]) + '.txt'
            parent_1 = np.loadtxt(parent_1_filename)
            parent_2 = np.loadtxt(parent_2_filename)
            weights_new = np.empty((8, 1))

            for j in range(8):
                parent_1_act = str(toBinary(parent_1[j]))
                parent_2_act = str(toBinary(parent_2[j]))

                print(parent_1_act)
                print(parent_2_act)

                cut = int(random.uniform(1, 31)) + 1
                weights_new_act = parent_1_act[:cut] + parent_2_act[cut:]

                listfromweight = list(weights_new_act)
                for l in range(len(weights_new_act)):
                    if random.uniform(0, 1/mutation) > 1/mutation - 1:
                        if listfromweight[l] == '1':
                            listfromweight[l] = '0'
                        elif listfromweight[l] == '0':
                            listfromweight[l] = '1'
                weights_new_act = ''.join(listfromweight)
                weights_new[j] = toDecimal(weights_new_act)
            kiment_nev = 'seged_weights' + str(i+1) + '.txt'
            np.savetxt(kiment_nev, weights_new)
        for i in range(population):
            seged = np.loadtxt('seged_weights' + str(i+1) + '.txt')
            np.savetxt('weights'+str(i+1)+'.txt', seged)
        fittnesses = open('avg_fittness.txt', 'a')
        fittnesses.write(str(sum(fittness)/population) + '\n')
        fittnesses.close()
