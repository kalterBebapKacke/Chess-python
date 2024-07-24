import multiprocessing as mp
import time
import cach
from multiprocessing.managers import SharedMemoryManager

def test(max=0):
    if max != 3:
        time.sleep(2)
        print(f'current:{max} ')
        p = mp.Pool(2)
        p.map(test, [max+1 for x in range(5)])

def test1(c):
    c.add(test='1')
    time.sleep(7)

def test2(c):
    c.add(test2777='1')
    print(c.get('test'))
    print(c.keys)
    print(c.value)

def test3(list):
    list.append('1')
    time.sleep(1)

def test4(list):
    time.sleep(3)
    print(list)

if __name__ == '__main__':
    smm, keys, value, length, _lenght = cach.setup()
    c = cach.cache(None, keys, value, length, _lenght)
    p1 = mp.Process(target=test2, args=(c,))
    p2 = mp.Process(target=test2, args=(c,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    cach.save(keys, value)