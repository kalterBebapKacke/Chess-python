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
    time.sleep(5)
    c.get('test')

def test3(list):
    list.append('1')
    time.sleep(1)

def test4(list):
    time.sleep(3)
    print(list)

if __name__ == '__main__':
    smm = SharedMemoryManager()
    smm.start()

    length = 100
    keys = smm.ShareableList(range(length))
    value = smm.ShareableList([0 for x in range(length)])
    c = cach.cache(smm, keys, value)
    p1 = mp.Process(target=test3, args=(keys,))
    p2 = mp.Process(target=test4, args=(keys,))
    p1.start()
    p2.start()