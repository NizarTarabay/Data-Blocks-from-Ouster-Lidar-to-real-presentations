# Added a comment

import csv
import os
import numpy as np
import struct
os. chdir("/home/etudiant/PycharmProjects/word6_to_32bitfloat-x-axis-g-")


def reorder(arr, index, n):
    '''

    :param arr: array to reorder
    :param index: reordering according to this index
    :param n: length of the array
    :return: the ordered array
    '''
    temp = [0] * n;

    # arr[i] should be
    # present at index[i] index
    for i in range(0, n):
        temp[index[i]] = arr[i]

        # Copy temp[] to arr[]
    for i in range(0, n):
        arr[i] = temp[i]
        index[i] = i
    return arr

def IMU_data ( file_csv, word):
    with open(file_csv) as csvfile:
        readCSV = csv.reader(csvfile)
        next(readCSV)  # skip header
        h = sum(1 for row in readCSV)

    with open(file_csv) as csvfile:
        readCSV = csv.reader(csvfile)
        next(readCSV)  # skip header
        w = 4
        data_block = [[1 for x in range(w)] for y in range(h)]
        j = 0
        for row in readCSV:
            row = np.asarray(row)
            # print (row[25:29])
            temp = row[(int(word)+1)*4-3:(int(word)+1)*4-3+4]
            # print (temp)
            four_bytes = reorder(temp, [3, 2, 1, 0], 4)
            i = 0
            for word in four_bytes:
                # four_bytes[i] = bin(int(word))
                data_block[j][i] = "{:08b}".format(int(word))
                i += 1
            j += 1
    return data_block




with open('bagfile-_os1_node_imu_packets.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    next(readCSV)  # skip header
    h = sum(1 for row in readCSV)

with open('bagfile-_os1_node_imu_packets.csv') as csvfile:
    readCSV = csv.reader(csvfile)
    next(readCSV)  # skip header
    w = 4
    word6 = [[1 for x in range(w)] for y in range(h)]
    j = 0
    for row in readCSV:
        row = np.asarray(row)
        # print (row[25:29])
        temp = row[45:49]
        # print (temp)
        four_bytes = reorder(temp, [3,2,1,0], 4)
        i = 0
        for word in four_bytes:
            # four_bytes[i] = bin(int(word))
            word6[j][i] = "{:08b}".format(int(word))
            i += 1
        j += 1

print(word6)
i = 0
float_xacc = []
for thirtytwobit in word6:
    four_bytes = ''.join(thirtytwobit[0:4])
    float_xacc.append(struct.unpack('!f', struct.pack('!I', int(four_bytes, 2)))[0])

import matplotlib.pyplot as plt
plt.plot(float_xacc)
plt.ylabel('x_axis angular velocity (deg per second)__')
plt.show()

import matplotlib.pyplot as plt
plt.plot(float_xacc)
plt.ylabel('x_axis angular velocity (deg per second)__')
plt.show()
