# Author: Nizar Tarabay
# Licence:
# This code extract IMU data from ouster bag2csv file IMU packets
# for more information on the IMU data block go to:
# Software User Guide Release v1.11.0 OS-1-64/16 High Resolution Imaging Lidar, section 3.5 IMU Data Format
# Prerequisite: Bag file generated from Lidar sensor and converted to CSV file

import csv
import os
import numpy as np
import struct
import matplotlib.pyplot as plt
os. chdir("/home/etudiant/PycharmProjects/word6_to_32bitfloat-x-axis-g-")

# ===================== array reordering ===================== #
def reorder(arr, index, n):
    '''
    this function reorder any array according to a specific index
    :param arr: array to reorder
    :param index: reordering according to this index
    :param n: length of the array
    :return: the ordered array
    '''
    temp = [0] * n

    # arr[i] should be
    # present at index[i] index
    for i in range(0, n):
        temp[index[i]] = arr[i]

        # Copy temp[] to arr[]
    for i in range(0, n):
        arr[i] = temp[i]
        index[i] = i
    return arr


# ===================== CSV 2 word_(4 Bytes) ===================== #
def IMU_data ( file_csv, word):
    '''
    :param file_csv: bag file convert to csv
    :param word: # of the word (only 32 bit) from the IMU packets (word takes values: 6-7-8-9-10-11)
    :return: list, each item in the list is a list with 4 Bytes
    '''
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
            for word1 in four_bytes:
                # four_bytes[i] = bin(int(word))
                data_block[j][i] = "{:08b}".format(int(word1))
                i += 1
            j += 1
    return data_block


# ===================== Convert word 2 float ===================== #
def convert_Bytes2float (word):
    '''
    :param word: one word four Bytes
    :return: 32 bit float representation of the word
    '''
    IMU_float = []
    for thirtytwobit in word:
        four_bytes = ''.join(thirtytwobit[0:4])
        IMU_float.append(struct.unpack('!f', struct.pack('!I', int(four_bytes, 2)))[0])
    return IMU_float


word6 = IMU_data('bagfile-_os1_node_imu_packets.csv', 6)
word7 = IMU_data('bagfile-_os1_node_imu_packets.csv', 7)
word8 = IMU_data('bagfile-_os1_node_imu_packets.csv', 8)
word9 = IMU_data('bagfile-_os1_node_imu_packets.csv', 9)
word10 = IMU_data('bagfile-_os1_node_imu_packets.csv', 10)
word11 = IMU_data('bagfile-_os1_node_imu_packets.csv', 11)


def plot (list, x_label, y_label):
    plt.plot(list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


# ===================== Plot IMU data block ===================== #
plot(convert_Bytes2float(word6), 'Time[]', 'Acceleration in x-axis (g)')
plot(convert_Bytes2float(word7), 'Time[]', 'Acceleration in y-axis (g)')
plot(convert_Bytes2float(word8), 'Time[]', 'Acceleration in z-axis (g)')
plot(convert_Bytes2float(word9), 'Time[]', 'Angular Velocity in x-axis (deg per second)')
plot(convert_Bytes2float(word10), 'Time[]', 'Angular Velocity in y-axis (deg per second)')
plot(convert_Bytes2float(word11), 'Time[]', 'Angular Velocity in z-axis (deg per second)')

