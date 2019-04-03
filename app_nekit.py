import multiprocessing
import time
import numpy as np
import os
import math
import tempfile
import shutil
import os
import sys
import heapq

def sort(data):
    data = np.sort(data, kind='quicksort')
    return data

def merge(files, memory_usage, tmp_dir):
    #Если пришел один файл значит он уже отсортирован
    if len(files) <= 1:
        return False

    memory_usage = int(memory_usage / len(files))
    # Создаем временный файл
    with tempfile.NamedTemporaryFile(mode="wb", dir=tmp_dir, delete=False) as tmp:
        #print(tmp.name, file=sys.stderr)
        handlers = [open(os.path.join('test', f), "rb") for f in files]
        merge = (map(int, np.fromfile(handle, dtype=np.uint32)) for handle in handlers)
        sortedMerge = heapq.merge(*merge)

        tmp_arr = []
        for item in sortedMerge:
            np.asarray(item, dtype=np.uint32).tofile(tmp)



if __name__ == '__main__':
    # Генератор файлов, перед тем как будешь кидать удали, т.к он самописный
    from app.Illuminate.generator import Generator
    Generator(file_name='tst', file_size='100MB', array_size=1000).generate()

    # Чем больше значение тем быстрее будет работать прога, но тем больше памяти будет жрать
    # Проверь сколько будет работать прога у тебя
    spd = 3

    start = time.time()
    cwd = os.getcwd()

    #Константы
    file_name = 'tst'
    # Memory 128 MB
    memory = 1024 * 1024 * 128
    # Папка для временных файлов
    tmp_dir = os.path.join(cwd, 'test')

    # Очищаем директорию с временными файлами
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

    os.mkdir(tmp_dir)

    # Сколько ядер
    processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=processes)

    # Делим память на размер uint32 для каждого процесса
    memory = int( memory / (np.dtype(np.uint32).itemsize*processes))

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
        ret = pool.map(sort, np.asarray(num, dtype=np.uint32))

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(mode="wb", dir=os.getcwd() + '/test', delete=False) as tmp:
            # Записываем туда отсортированные данные
            np.asarray(ret, dtype=np.uint32).tofile(tmp)

    pool.close()
    pool.join()

    print("Time Sort: ", time.time() - start)
    print("---------------------")

    from itertools import product

    pool = multiprocessing.Pool(processes=processes)
    while True:
        # Получаем дескрипторы файлов из директории test/
        files_in_test_dir = [f for f in os.listdir(tmp_dir) if os.path.isfile(os.path.join(tmp_dir, f))]

        #print(files_in_test_dir)

        if len(files_in_test_dir) <= 1:

            shutil.move( os.path.join(tmp_dir, files_in_test_dir[0]), os.getcwd() + '/output')
            break

        files_in_test_dir = files_in_test_dir[:2]

        # Паралельная сортировка на всех ядрах
        size = int(math.ceil(float(len(files_in_test_dir)) / processes))
        size = max([ size, 2])

        f = [files_in_test_dir[i * size:(i + 1) * size] for i in range(processes)]

        arg_list = [[f[i], memory, tmp_dir] for i in range(processes)]
        ret = pool.starmap(merge, arg_list)

        for f in files_in_test_dir:
            os.unlink(os.path.join(tmp_dir, f))



    pool.close()
    pool.join()

    print("Time elapsed: ", time.time() - start)