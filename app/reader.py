import numpy as np

class BinaryReader:
    def __init__(self, file_name: str = 'data_temp', how_many=1024 * 1024 * 8):
        self.file_name = file_name
        self.how_many = how_many

    def read(self):
        f = open(self.file_name, 'rb')
        val = np.fromfile(f, dtype=np.uint32, count=self.how_many)
        print(len(val))