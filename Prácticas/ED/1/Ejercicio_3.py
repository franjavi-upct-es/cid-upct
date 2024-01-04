import sys
data = []
for k in range(27):
    a = len(data)
    b = sys.getsizeof(data)
    print(f'Longitud: {a}; Tamaño en bytes: {b}')
    data.append(None)