l = [[4, -1], [1, -3]]
depth = 2

def iterate(List):
    _l = list()
    for i, x in enumerate(List):
        print(x)
        if not isinstance(x, list):
            _l.append(f'Zahl: {x}')
        else:
            _l.append(iterate(x))
    return _l

print(iterate(l))



