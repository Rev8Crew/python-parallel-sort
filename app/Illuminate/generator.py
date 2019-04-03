import random
import os
import numpy as np
import time

class Generator:
    def __init__(self, **kwargs):
        """
        :param file_name - name of output file\n
        :param file_size - size of output file\n
        :param min_value - min random value of elem\n
        :param max_value - max random value of elem\n
        :param array_size - speed up generating(100, 1000, 10000)
        """
        self.file_name = self.__get_value(kwargs, 'file_name', 'data_temp')
        self.file_size = self.__get_value(kwargs, 'file_size', '1024MB')

        self.min_value = self.__get_value(kwargs, 'min_value', 1)
        self.max_value = self.__get_value(kwargs, 'max_value', 100)

        self.array_size = self.__get_value(kwargs, 'array_size', 1000)

    def generate(self):
        file = open(self.file_name, mode='wb')

        fsize = self.__convert_file_size(self.file_size)
        fsize = round(fsize / self.array_size)
        #Progress
        proc_25 = 0.25
        proc_50 = 0.5
        proc_75 = 0.75

        start = time.clock()

        for i in range(fsize):
            progress = i / fsize

            if progress >= proc_25 and proc_25:
                print("Progres[25%] ->", time.clock() - start)
                proc_25 = 0.0

            if progress >= proc_50 and proc_50:
                print("Progres[50%] ->", time.clock() - start)
                proc_50 = 0.0

            if progress >= proc_75 and proc_75:
                print("Progres[75%] ->", time.clock() - start)
                proc_75 = 0.0

            x = np.random.randint(1, 1000, size=self.array_size, dtype=np.uint32)
            #print(x)
            file.write(x)

        print("Time spent in (Generator->generate) is: ", time.clock() - start)

        file.close()

    @staticmethod
    def __get_value(kwargs: dict, key, default):
        return kwargs[key] \
            if key in kwargs.keys()\
            else default

    @staticmethod
    def __convert_file_size(file_size: str):
        if 'GB' in file_size:
            file_size = int(file_size.replace('GB', ''))
            file_size = str(int(file_size) * 1024) + 'MB'

        if 'MB' in file_size:
            file_size = int(file_size.replace('MB', ''))
            file_size *= 1000000/4

        return int(file_size)

    @staticmethod
    def __get_file_size(file: str):
        return os.path.getsize(filename=file)

