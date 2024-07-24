import os.path
from multiprocessing import shared_memory, Manager
from multiprocessing import Process, Value, Array
#from shared_memory_dict import SharedMemoryDict
from multiprocessing.managers import SharedMemoryManager
import json

def setup(length=100):
    smm = SharedMemoryManager()
    smm.start()
    _keys, _value = load()
    _length = len(_keys)
    for x in range(length):
        _keys.append(0)
        _value.append(0)

    length += _length
    keys = smm.ShareableList(_keys)
    value = smm.ShareableList(_value)

    return smm, keys, value, length, _length

def save(keys, value):
    d = dict()
    keys = list(keys)
    value = list(value)
    for x in range(len(keys)):
        if 0 in keys:
            del keys[keys.index(0)]
        if 0 in value:
            del value[value.index(0)]
    print(f'keys: {keys}')
    for i in range(len(keys)):
        d[keys[i]] = value[i]
    print(d)
    with open('cache.json', 'w') as file:
        file.write(json.dumps(d))

def load():
    if not os.path.exists('cache.json'):
        f = open('cache.json', 'w')
        f.write('{}')
    with open('cache.json', 'r') as file:
        cache = file.read()
        if cache != '':
            cache = json.loads(cache)
            keys = cache.keys()
            keys = list(keys)
            value = cache.values()
            value = list(value)
            return keys, value
        else:
            return [], []

class cache:

    def __init__(self, smm, keys, value, len, cur_length):
        self.smm = smm
        self.keys = keys
        self.value = value
        self.current = cur_length
        self.len = len

    def __del__(self):
        try:
            self.smm.shutdown()
        except Exception as ee:
            print(ee)

    def add(self, **kwargs):
        if self.current == self.len - 1:
            print('Cache is full')
            return None
        for x in kwargs.keys():
            self.current += 1
            self.keys[self.current - 1] = str(x)
            self.value[self.current - 1] = str(kwargs[x])


    def get(self, *args):
        _return = list()
        for x in args:
            if str(x) in self.keys:
                index = self.keys.index(str(x))
                _return.append(self.value[index])
        return _return
