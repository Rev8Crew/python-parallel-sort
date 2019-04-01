import multiprocessing
import sys
import time

import numpy as np

import os
import math
import tempfile

class SplitFile:

    def __init__(self, big_file, memory):

        self.big_file = big_file
        self.memory = memory

    def read(self) -> list:
        return np.fromfile(self.big_file, count=self.memory, dtype=np.uint32).tolist()


    def sort_tmp(self, data):
        start = time.time()
        print("Start at ", start)

        data = np.sort(data, kind='mergesort')

        print("Time elapsed by sorting: ", time.time() - start, type(data),  file=sys.stderr)

    def split(self):

        processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=processes)

        while True:
            bytes = self.read()

            if not bytes:
                break

            #Паралельная сортировка
            size = int(math.ceil(float(len(bytes)) / processes))
            bytes = [bytes[i * size:(i + 1) * size] for i in range(processes)]

            print('Len:', len(bytes), 'Size:', size)
            pool.map(self.sort_tmp, bytes)


        pool.close()
        pool.join()
