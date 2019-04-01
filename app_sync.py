import heapq
import multiprocessing
import sys
import time

import numpy as np

import os
import math
import tempfile

import shutil

import psutil


file = 'data_temp'

class SplitFile:

    tmp = 'tmp'

    def __init__(self, big_file, memory):

        self.big_file = big_file
        self.memory = int(memory / np.dtype(np.int32).itemsize)

        self.clear_tmp_dir()
        self.create_tmp_dir()

    def create_tmp_dir(self):

        if os.path.exists(os.path.join(os.getcwd(), self.tmp)):
            return True

        return os.mkdir(os.path.join(os.getcwd(), self.tmp))

    def clear_tmp_dir(self):
        if os.path.exists(os.path.join(os.getcwd(), self.tmp)) is False:
            return True

        return shutil.rmtree(os.path.join(os.getcwd(), self.tmp))

    def get_files_tmp_dir(self):
        files = [f for f in os.listdir(self.tmp) if os.path.isfile(os.path.join(self.tmp, f))]
        return files

    def read(self, f) -> list:
        return np.fromfile(f, count=self.memory, dtype=np.uint32)

    def sort_tmp(self, data):
        data: np.array = np.sort(data)

        tmp = tempfile.NamedTemporaryFile(mode="w+", dir=os.getcwd() + '/tmp', delete=False)
        data.tofile(tmp, '\n')

        tmp.close()

    def split(self):
        processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=processes)

        f = open(self.big_file, 'rb')
        while True:
            bytes = self.read(f)

            if not len(bytes):
                break

            # Паралельная сортировка
            size = int(math.ceil(float(len(bytes)) / processes))
            bytes = [bytes[i * size:(i + 1) * size] for i in range(processes)]

            pool.map(self.sort_tmp, bytes)

        pool.close()
        pool.join()

    def mergeSortedtempFiles(self):

        ttmp = []
        for tmp in self.get_files_tmp_dir():
            f = open(os.path.join( os.getcwd(), 'tmp', tmp), 'r')
            ttmp.append(f)

        mergedNo = (map(int, tempFileHandler) for tempFileHandler in
                    ttmp)  # mergedNo is a generator which stores all the sorted number in ((1,4,6),(3,7,8)...) format. Since it's generator ,it doesn't stores in memory and do lazy allocation
        sortedCompleteData = heapq.merge(
            *mergedNo)  # uses python heapqmodule that takes a list of sorted iterators and sort it and generates a sorted iterator , So again no more storing of data in memory
        return sortedCompleteData

if __name__ == '__main__':
    memory = int(1048576 * 128 / 4)
    print('Start Memory:',psutil.virtual_memory())
    print('Allocated to program:', memory )
    start = time.time()

    sp = SplitFile(file, memory)

    sp.split()
    print('Split File end in ', time.time() - start)
    sortedCompleteData = sp.mergeSortedtempFiles()

    output = open('output.txt', "w")

    tmpArr = []
    for item in sortedCompleteData:
        tmpArr.append(str(item))

        if len(tmpArr) >= 1048576:
            np.asarray(tmpArr, dtype=np.uint32).tofile(output, '\n')
            tmpArr = []

    if len(tmpArr):
        output.write('\n'.join(tmpArr))

    tmpArr = []

    print('End Memory:', psutil.virtual_memory())
    print("Time elapsed by split: ", time.time() - start)
    print("Files in dir:", sp.get_files_tmp_dir())