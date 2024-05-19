a = '132454567564556532465436345'
a = list(a)
print(a.__contains__('1'))
print(a.index('1'))
del a[2:7]
a = ''.join(a)
print(a)

