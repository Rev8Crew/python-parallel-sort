import numpy as np

class BinaryPrinter:
    def __init__(self, file_name: str = 'data_temp', how_many=4):
        self.file_name = file_name
        self.how_many = how_many

    def print(self):
        f = open(self.file_name, 'rb')
        print(np.fromfile(f, dtype=np.uint32, count=self.how_many))

