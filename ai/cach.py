from multiprocessing import shared_memory, Manager
from multiprocessing import Process, Value, Array
from shared_memory_dict import SharedMemoryDict
from multiprocessing.managers import SharedMemoryManager

def setup():
    smm = SharedMemoryManager()
    smm.start()

    length = 100
    keys = smm.ShareableList(range(length))
    value = smm.ShareableList([0 for x in range(length)])

    return smm, keys, value


class cache:

    def __init__(self, smm, keys, value):
        self.smm = smm
        self.keys = keys
        self.value = value

    def __del__(self):
        try:
            self.smm.shutdown()
        except Exception as ee:
            print(ee)

    def add(self, **kwargs):
        for x in kwargs.keys():
            self.keys.append(str(x))
            self.value.append(str(kwargs[x]))

    def get(self, *args):
        _return = list()
        for x in args:
            if str(x) in self.keys:
                index = self.keys.index(str(x))
                _return.append(self.value[index])
        return _return
