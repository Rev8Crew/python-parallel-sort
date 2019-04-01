import multiprocessing.dummy as multiprocessing
import time

def a():
    time.sleep(2)
    return 'a'
def b():
    time.sleep(2)
    return 'b'
def c():
    time.sleep(1)
    return 'c'

p = multiprocessing.Pool()

results = p.map(lambda f: f(),[a,b,c])
print(results)
p.close()
p.join()