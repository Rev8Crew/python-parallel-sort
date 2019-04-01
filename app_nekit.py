import heapq
import multiprocessing
import time
import numpy as np
import os
import math
import tempfile
import shutil


def sort(data):
    #Создаем временный файл
    tmp = tempfile.NamedTemporaryFile(mode="w+", dir=os.getcwd() + '/test', delete=False)
    #Записываем туда отсортированные данные
    np.sort(data).tofile(tmp, '\n')

if __name__ == '__main__':

    # Генератор файлов, перед тем как будешь кидать удали, т.к он самописный
    from app.Illuminate.generator import Generator
    Generator(file_name='tst', file_size='1GB', array_size=1000).generate()

    # Чем больше значение тем быстрее будет работать прога, но тем больше памяти будет жрать
    # Проверь сколько будет работать прога у тебя
    spd = 5

    start = time.time()
    cwd = os.getcwd()

    #Константы
    file_name = 'tst'
    # Memory 128 MB
    memory = 1024 * 1024 * 128
    # Папка для временных файлов
    tmp_dir = os.path.join( cwd, 'test')

    # Очищаем директорию с временными файлами
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.mkdir(tmp_dir)

    # Сколько ядер
    processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=processes)

    # Делим память на размер uint32
    memory = int( memory / np.dtype(np.int32).itemsize)

    f = open(file_name, 'rb')
    while True:
        # Считываем memory MB данных из файла
        num = np.fromfile(f, count=memory, dtype=np.uint32)

        if not len(num):
            num = None
            break

        # Паралельная сортировка на всех ядрах
        size = int(math.ceil(float(len(num)) / processes))
        num = [num[i * size:(i + 1) * size] for i in range(processes)]

        # Запускаем сортировку
        pool.map(sort, num)

    pool.close()
    pool.join()

    # Получаем дескрипторы файлов из директории test/
    files_in_test_dir = [open(os.path.join(tmp_dir, f), "r") for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]

    # Создаем генератор, чтобы не тратить всю память
    merge = (map(int, tempFileHandler) for tempFileHandler in files_in_test_dir)
    sortedMerge = heapq.merge(*merge)

    final = open('final.txt', "w")

    tmp_arr = []
    for item in sortedMerge:
        tmp_arr.append(str(item))

        # Записываем не по одному числу а по 1 MB данных
        if len(tmp_arr) >= 1048576 * spd:
            np.asarray(tmp_arr, dtype=np.uint32).tofile(final, '\n')
            tmp_arr = []

    if len(tmp_arr):
        final.write('\n'.join(tmp_arr))

    print("Time elapsed: ", time.time() - start)