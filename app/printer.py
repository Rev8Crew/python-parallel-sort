import numpy as np

from binaryornot.check import is_binary


class Printer:
    def __init__(self, file_name: str = 'data_temp', how_many=100):
        """
        Print file content limited by :how_many
        :param file_name:
        :param how_many:
        """
        self.file_name = file_name
        self.how_many = how_many

    def is_binary(self):
        return is_binary(self.file_name)

    def print(self):
        binary = self.is_binary()
        f = open(self.file_name, 'rb') if binary else open(self.file_name, 'r')
        data = np.fromfile(f, dtype=np.uint32)
        ff = open('log.txt', 'w')
        for item in list(data):
            ff.write( str(item) + '\n')

Printer('tmpxk_u26f9').print()