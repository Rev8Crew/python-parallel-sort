#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import tempfile
import heapq
import sys
import numpy as np
import time
import multiprocessing
import math


class heapnode:
    """ Heapnode of a Heap (MinHeap Here)
       @params
               item        The actual value to be stored in heap
               fileHandler The filehandler of the file that stores the number"""

    def __init__(
            self,
            item,
            fileHandler,
    ):
        self.item = item
        self.fileHandler = fileHandler

class externamMergeSort:
    """ Splits the large file into small files ,sort the small files and uses python
        heapq module to merge the different small sorted files.  Each sorted files is
        loaded as a  generator ,hence won't loads entire data into memory """
    """ @params
           sortedTempFileHandlerList - List of all filehandlers to all temp files formed by splitting large files
    """

    def __init__(self):
        manager = multiprocessing.Manager()
        self.sortedTempFileHandlerList = manager.list()
        self.getCurrentDir()

    def getCurrentDir(self):
        self.cwd = os.getcwd()

    """ Iterates the sortedCompleteData Generator """

    def iterateSortedData(self, sortedCompleteData):
        for no in sortedCompleteData:
            print(no)

    """ HighLevel Pythonic way to sort all numbers in the list of files that are pointed by Filehandlers of sortedTempFileHandlerList """

    def mergeSortedtempFiles(self):
        mergedNo = (map(int, tempFileHandler) for tempFileHandler in
                    self.sortedTempFileHandlerList)  # mergedNo is a generator which stores all the sorted number in ((1,4,6),(3,7,8)...) format. Since it's generator ,it doesn't stores in memory and do lazy allocation
        sortedCompleteData = heapq.merge(
            *mergedNo)  # uses python heapqmodule that takes a list of sorted iterators and sort it and generates a sorted iterator , So again no more storing of data in memory
        return sortedCompleteData

    """ min heapify function """

    def heapify(
            self,
            arr,
            i,
            n,
    ):
        left = 2 * i + 1
        right = 2 * i + 2
        if left < n and arr[left].item < arr[i].item:
            smallest = left
        else:
            smallest = i

        if right < n and arr[right].item < arr[smallest].item:
            smallest = right

        if i != smallest:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            self.heapify(arr, smallest, n)

    """ construct heap """

    def construct_heap(self, arr):
        l = len(arr) - 1
        mid = l // 2
        while mid >= 0:
            self.heapify(arr, mid, l)
            mid -= 1

    """ low level implementation to merge k sorted small file to a larger file . Move first element of all files to a min heap . The Heap has now the smallest element .
         Mmoves  that element from heap to a file . Get the filehandler of that element .Read the next element using the  same filehandler . If next file element is empty, mark it as INT_MAX.
         Moves it to heap . Again Heapify . Continue this until all elements of heap is INT_MAX or all the smaller files have read fully """

    def mergeSortedtempFiles_low_level(self):
        list = []
        sorted_output = []
        for tempFileHandler in self.sortedTempFileHandlerList:
            item = int(tempFileHandler.readline().strip())
            list.append(heapnode(item, tempFileHandler))

        self.construct_heap(list)
        while True:
            min = list[0]
            if min.item == sys.maxsize:
                break
            sorted_output.append(min.item)
            fileHandler = min.fileHandler
            item = fileHandler.readline().strip()
            if not item:
                item = sys.maxsize
            else:
                item = int(item)
            list[0] = heapnode(item, fileHandler)
            self.heapify(list, 0, len(list))
        return sorted_output

    """ function to Split a large files into smaller chunks , sort them and store it to temp files on disk"""
    '''
    def splitFiles(self, largeFileName, smallFileSize):
        largeFileHandler = open(largeFileName,"rb")
        while True:
            numbers=np.fromfile(largeFileHandler,count=smallFileSize,dtype=np.uint32).tolist()
            if not numbers:
                break
            start_sorting = time.time()
            numbers = self.merge_sort_parallel(numbers)
            #numbers = sorted(numbers)
            end_sorting = time.time() - start_sorting
            print("Time elapsed by sorting: ", end_sorting)
            tempFile = tempfile.NamedTemporaryFile(mode="w+", dir=self.cwd
                                                       + '/temp', delete=False)
            start_temp = time.time()
            for item in numbers:
                tempFile.write(str(item)+'\n')
            end_temp = time.time() - start_temp
            print("Time elapsed by temp: ", end_temp)
            tempFile.seek(0)
            self.sortedTempFileHandlerList.append(tempFile)'''

    def splitFiles(self, largeFileName, smallFileSize):
        largeFileHandler = open(largeFileName, "rb")
        processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=processes)
        while True:
            numbers = np.fromfile(largeFileHandler, count=smallFileSize, dtype=np.uint32).tolist()
            if not numbers:
                break
            size = int(math.ceil(float(len(numbers)) / processes))
            numbers= [numbers[i * size:(i + 1) * size] for i in range(processes)]
            files = pool.map(self.splitFilesParallel, numbers)


    def splitFilesParallel(self,data):
        start_sorting = time.time()
        numbers = sorted(data)
        end_sorting = time.time() - start_sorting
        print("Time elapsed by sorting: ", end_sorting)
        tempFile = tempfile.NamedTemporaryFile(mode="w+", dir=self.cwd
                                                              + '/temp', delete=False)
        start_temp = time.time()
        for item in numbers:
            tempFile.write(str(item) + '\n')
        end_temp = time.time() - start_temp
        print("Time elapsed by temp: ", end_temp)
        tempFile.seek(0)
        self.sortedTempFileHandlerList.append(tempFile)

    def merge(self, *args):
        # Support explicit left/right args, as well as a two-item
        # tuple which works more cleanly with multiprocessing.
        left, right = args[0] if len(args) == 1 else args
        left_length, right_length = len(left), len(right)
        left_index, right_index = 0, 0
        merged = []
        while left_index < left_length and right_index < right_length:
            if left[left_index] <= right[right_index]:
                merged.append(left[left_index])
                left_index += 1
            else:
                merged.append(right[right_index])
                right_index += 1
        if left_index == left_length:
            merged.extend(right[right_index:])
        else:
            merged.extend(left[left_index:])
        return merged

    def merge_sort(self, data):
        length = len(data)
        if length <= 1:
            return data
        middle = length // 2
        left = self.merge_sort(data[:middle])
        right = self.merge_sort(data[middle:])
        return self.merge(left, right)


    def merge_sort_parallel(self, data):
        # Creates a pool of worker processes, one per CPU core.
        # We then split the initial data into partitions, sized
        # equally per worker, and perform a regular merge sort
        # across each partition.
        # start = time.time()
        processes = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=processes)
        size = int(math.ceil(float(len(data)) / processes))
        data = [data[i * size:(i + 1) * size] for i in range(processes)]
        data = pool.map(self.merge_sort, data)

        # end = time.time() - start
        # print(end)
        # Each partition is now sorted - we now just merge pairs of these
        # together using the worker pool, until the partitions are reduced
        # down to a single sorted result.
        while len(data) > 1:
            # If the number of partitions remaining is odd, we pop off the
            # last one and append it back after one iteration of this loop,
            # since we're only interested in pairs of partitions to merge.
            extra = data.pop() if len(data) % 2 == 1 else None
            data = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
            data = pool.map(self.merge, data) + ([extra] if extra else [])
        return data[0]


if __name__ == '__main__':
    start_program = time.time()
    largeFileName = sys.argv[1]
    smallFileSize = 50000000
    obj = externamMergeSort()
    start_split = time.time()
    obj.splitFiles(largeFileName, smallFileSize)
    end_split = time.time() - start_split
    print("Time elapsed by split: ", end_split)
    start_merge = time.time()
    sortedCompleteData = obj.mergeSortedtempFiles()
    end_merge = time.time() - start_merge
    print("Time elapsed by merge: ", end_merge)
    start_writing = time.time()
    output=open('output.txt',"w")
    for item in sortedCompleteData:
        output.write(str(item) + '\n')
    end_writing = time.time() - start_writing
    print("Time elapsed by writing: ", end_writing)
    end_program = time.time() - start_program
    print("Time elapsed by program: ", end_program)
