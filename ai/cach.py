from multiprocessing import shared_memory, Manager
from multiprocessing import Process, Value, Array
#from shared_memory_dict import SharedMemoryDict
from multiprocessing.managers import SharedMemoryManager

def setup():
    smm = SharedMemoryManager()
    smm.start()

    length = 100
    keys = smm.ShareableList([0 for x in range(length)])
    value = smm.ShareableList([0 for x in range(length)])

    return smm, keys, value


class cache:

    def __init__(self, smm, keys, value, len):
        self.smm = smm
        self.keys = keys
        self.value = value
        self.current = 0
        self.len = len

    def __del__(self):
        try:
            self.smm.shutdown()
        except Exception as ee:
            print(ee)

    def add(self, **kwargs):
        if self.current == self.len -1:
            print('Cache is full')
            return None
        for x in kwargs.keys():
            self.keys[self.current] = str(x)
            self.value[self.current] = str(kwargs[x])
            self.current += 1

    def get(self, *args):
        _return = list()
        for x in args:
            if str(x) in self.keys:
                index = self.keys.index(str(x))
                _return.append(self.value[index])
        return _return
